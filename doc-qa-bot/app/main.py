from fastapi import FastAPI, UploadFile, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Literal
from app.database import get_connection, init_db
from app.chunker import chunk_document
from app.embeddings import get_embeddings_batch
from app.rag import ask
from fastapi.middleware.cors import CORSMiddleware
import io

app = FastAPI(title="Document Q&A Bot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
def startup():
    init_db()

# Request/Response models
class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class QuestionRequest(BaseModel):
    question: str
    chat_history: list[ChatMessage] = Field(default_factory=list)

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

@app.post("/upload")
async def upload_document(file: UploadFile, background_tasks: BackgroundTasks):
    """Upload a document for processing."""

    # Validate file type
    allowed_types = [".txt", ".md", ".pdf"]
    if not any(file.filename.endswith(t) for t in allowed_types):
        raise HTTPException(400, f"File type not supported. Use: {allowed_types}")

    # Read content
    content = await file.read()

    # Handle different file types
    if file.filename.endswith(".pdf"):
        # You'd use PyPDF2 or pdfplumber here
        # For simplicity, assuming text extraction is done
        text = content.decode("utf-8", errors="ignore")
    else:
        text = content.decode("utf-8")

    # Create document record
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO documents (filename) VALUES (%s) RETURNING id",
            (file.filename,)
        )
        doc_id = cur.fetchone()["id"]
    conn.commit()
    conn.close()

    # Process in background
    background_tasks.add_task(process_document, doc_id, text, file.filename)

    return {"message": "Document uploaded", "document_id": doc_id, "status": "processing"}

@app.get("/documents")
async def list_documents():
    """List all uploaded documents and their status."""
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT id, filename, status, created_at FROM documents ORDER BY created_at DESC")
        docs = cur.fetchall()
    conn.close()
    return docs

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """Ask a question about the uploaded documents."""
    history = [message.model_dump() for message in request.chat_history]
    result = ask(request.question, history)
    return AnswerResponse(
        answer=result["answer"],
        sources=result["sources"]
    )