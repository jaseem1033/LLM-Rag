import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg2.connect(
        os.getenv("DATABASE_URL"),
        cursor_factory=RealDictCursor
    )

def init_db():
    conn = get_connection()
    with conn.cursor() as cur:
        # Enable pgvector
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector")

        # Documents table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                filename TEXT NOT NULL,
                status TEXT DEFAULT 'processing',
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)

        # Chunks table with embeddings
        cur.execute("""
            CREATE TABLE IF NOT EXISTS chunks (
                id SERIAL PRIMARY KEY,
                document_id INTEGER REFERENCES documents(id) ON DELETE CASCADE,
                content TEXT NOT NULL,
                embedding vector(1536),
                chunk_index INTEGER
            )
        """)

    conn.commit()
    conn.close()


init_db()