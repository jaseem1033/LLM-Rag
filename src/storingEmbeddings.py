from openai import OpenAI
import psycopg2

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)
conn = psycopg2.connect("postgresql://postgres:postgres@localhost:5433/vector_db")

def store_document(content: str):
    # Generate embedding
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=content
    )
    embedding = response.data[0].embedding

    # Store in Postgres
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
            (content, embedding)
        )
    conn.commit()

# Store some documents
store_document("How to reset your password: Go to Settings > Security > Reset Password")
store_document("Changing your email: Navigate to Profile > Edit > Email Address")
store_document("Billing FAQ: We accept Visa, Mastercard, and PayPal")