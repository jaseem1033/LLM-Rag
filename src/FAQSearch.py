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

class FAQSearch:
    def __init__(self):
        self._ensure_table()

    def _ensure_table(self):
        with conn.cursor() as cur:
            cur.execute("""
                        CREATE TABLE IF NOT EXISTS faqs
                        id SERIAL PRIMARY KEY,
                        question TEXT,
                        answer TEXT,
                        embedding vector(1536)
                        )
                    """)
        conn.commit()

    def add_faq(self, question: str, answer: str):
        embedding = self._get_embedding(question)
        with conn.cursor as cur:
            cur.execute(
                "INSERT INTO faqs (question, answer, embedding) VALUES(%s, %s, %s)",
                (question, answer, embedding)
            )
        conn.commit()
    
    def search(self, query: str, threshold: float = 0.7) -> dict | None:
        query_embedding = self._get_embedding(query)
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT question, answer, 1 - (embedding <=> %s::vector) AS similarity
                        FROM faqs
                        WHERE 1 - (embedding <=> %s::vector) > %s                        
"""
                
            )
