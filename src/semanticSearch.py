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
    api_key =  api_key
)

# PostgreSQL connection
conn = psycopg2.connect(
    "postgresql://postgres:postgres@localhost:5433/vector_db"
)


def semantic_search(query: str, limit: int = 1) -> list[dict]:
    # Generate embedding for the query
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    query_embedding = response.data[0].embedding
    
    # Find similar documents
    with conn.cursor() as cur:
        cur.execute("""
            SELECT content, 1 - (embedding <=> %s::vector) AS similarity
            FROM documents
            ORDER BY similarity DESC
            LIMIT %s
        """, (query_embedding, limit))

        results = []
        for row in cur.fetchall():
            results.append({
                "content": row[0],
                "similarity": round(row[1], 3)
            })
        return results


# Search!
results = semantic_search("I forgot my password")
for r in results:
    print(f"{Back.WHITE}{Fore.GREEN}{Style.BRIGHT} {r['similarity']}: {r['content'][:50]}...")
