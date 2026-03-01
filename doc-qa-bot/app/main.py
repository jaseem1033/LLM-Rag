from fastapi import FastAPI, UploadFile, HTTPException, BackgroundTasks
from pydantic import BaseModel
from app.database import get_connection, init_db
from app.chunker import chunk_document
from app.embeddings import get_embeddings_batch
from app.rag import ask
import io

app = FastAPI(title="Document Q&A Bot")

# Initialize database on startup
@app.on_event("startup")
def startup():
    init_db()

# Request/Response models
class QuestionRequest(BaseModel):
    question: str
    chat_history: list = None

class AnswerResponse(BaseModel):
    answer: str
    sources: list[str]

# Background task for document processing
def process_document(doc_id: int, content: str, filename: str):
    conn = get_connection()

    try:
        # Chunk the document
        chunks = chunk_document(content)

        # Generate embeddings in batch
        embeddings = get_embeddings_batch(chunks)

        # Store chunks with embeddings
        with conn.cursor() as cur:
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                cur.execute(
                    """INSERT INTO chunks (document_id, content, embedding, chunk_index)
                       VALUES (%s, %s, %s, %s)""",
                    (doc_id, chunk, embedding, i)
                )

            # Mark document as ready
            cur.execute(
                "UPDATE documents SET status = 'ready' WHERE id = %s",
                (doc_id,)
            )

        conn.commit()
        print(f"Processed {filename}: {len(chunks)} chunks")

    except Exception as e:
        # Mark as failed
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE documents SET status = 'failed' WHERE id = %s",
                (doc_id,)
            )
        conn.commit()
        print(f"Failed to process {filename}: {e}")

    finally:
        conn.close()