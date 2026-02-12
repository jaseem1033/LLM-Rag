from openai import OpenAI
import psycopg2
from pgvector.psycopg2 import register_vector

# OpenRouter / OpenAI client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"   # replace this
)

# PostgreSQL connection
conn = psycopg2.connect(
    "postgresql://postgres:postgres@localhost:5433/vector_db"
)

# Register pgvector type with psycopg2
register_vector(conn)


def semantic_search(query: str, limit: int = 5) -> list[dict]:
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
            LIMIT %s
        """, (query_embedding, limit))

        results = []
        for row in cur.fetchall():
            results.append({
                "content": row[0],
                "similarity": round(row[1], 3)
            })
        
        # Sort by similarity descending (highest first)
        # results.sort(key=lambda x: x["similarity"], reverse=True)
        return results


# Search!
results = semantic_search("I need to change my email")
for r in results:
    print(f"{r['similarity']}: {r['content'][:50]}...")
