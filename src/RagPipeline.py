from openai import OpenAI
import psycopg2
from colorama import Fore, Style, init, Back
import os
from dotenv import load_dotenv

load_dotenv()
init(autoreset=True)

api_key = os.getenv("OPEN_API_KEY")

# OpenRouter / OpenAI client
client = OpenAI(
    base_url = "https://openrouter.ai/api/v1",
    api_key = api_key
)

# PostgreSQL connection
conn = psycopg2.connect(
    "postgresql://postgres:postgres@localhost:5433/vector_db"
)

class RagPipeline:
    def __init__(self):
        self.min_similarity = 0.35
        self._ensure_table()
    
    def _ensure_table(self):
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS chunks (
                        id SERIAL PRIMARY KEY,
                        content TEXT,
                        source TEXT,
                        embedding vector(1536)
                    )
            """)
            conn.commit()
    
    def ingest_document(self, content: str, source: str):
        """Chunk and store document."""
        chunks = self._chunk_text(content)
        for chunk in chunks:
            embedding = self._get_embedding(chunk)
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO chunks (content, source, embedding) VALUES (%s, %s, %s)",
                    (chunk, source, embedding)
                )
            conn.commit()
            print(f"Ingested {len(chunks)} chunks from {source}")

    def query(self, question: str, top_k: int = 3) -> str:
        """RAG query: retrieve context, then generate answer."""

        context_chunks = self._retrieve(question, top_k)

        if not context_chunks:
            return "I don't have information about that."
        
        context = "\n\n".join([c['content'] for c in context_chunks])
        best_chunk = max(context_chunks, key=lambda c: c["similarity"])
        sources = list(set([c['source'] for c in context_chunks]))

        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are a RAG assistant.
                    Use ONLY the provided context.
                    If the user input is a statement, summarize the key facts from context.
                    If the context truly does not contain the answer, reply exactly: I don't have information about that.
                    Keep it concise."""
                },
                {
                    "role": "user",
                    "content": f"""Context: {context}
                    Question: {question}"""
                }
            ],
            temperature=0
        )

        answer = (response.choices[0].message.content or "").strip()

        if (
            "i don't have information about that" in answer.lower()
            and best_chunk["similarity"] >= self.min_similarity
        ):
            answer = f"Based on available documents: {best_chunk['content']}"

        return f"{answer}\n\nSources: {', '.join(sources)}"
    
    def _retrieve(self, query: str, top_k: int) -> list[dict]:
        """Find most relevant chunks."""
        query_embedding = self._get_embedding(query)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT content, source, 1 - (embedding <=> %s::vector) AS similarity
                FROM chunks
                ORDER BY embedding <=> %s::vector
                LIMIT %s
            """, (query_embedding, query_embedding, top_k))
            rows = [
                {"content": r[0], "source": r[1], "similarity": float(r[2])}
                for r in cur.fetchall()
            ]
            return [row for row in rows if row["similarity"] >= self.min_similarity]
    
    def _chunk_text(self, text: str, size: int = 300, overlap: int = 30) -> list[str]:
        words = text.split()
        chunks = []
        start = 0
        while start < len(words):
            chunk = ' '.join(words[start:start + size])
            chunks.append(chunk)
            start += size - overlap
        return chunks
    
    def _get_embedding(self, text: str) -> list[float]:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
