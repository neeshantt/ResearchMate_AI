
import os
import uuid
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field

from backend.database import (
    initialize_database,
    save_document,
    get_document,
    get_all_documents,
    delete_document as delete_document_record
)

from backend.services.document_service import (
    process_document,
    ask_document_question
)

from backend.services.persistent_store import (
    save_faiss_index,
    load_faiss_index,
    delete_faiss_index
)


BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


app = FastAPI(
    title="ResearchMate AI",
    description="AI-powered PDF Summarization and Question Answering",
    version="2.0.0"
)


@app.on_event("startup")
def startup():
    initialize_database()


class QuestionRequest(BaseModel):
    document_id: str
    question: str = Field(min_length=1)


@app.get("/")
def home():
    return {
        "message": "Welcome to ResearchMate AI",
        "status": "Running"
    }


@app.post("/upload-pdf")
def upload_pdf(file: UploadFile = File(...)):

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are allowed.")

    document_id = str(uuid.uuid4())
    pdf_path = UPLOAD_DIR / f"{document_id}.pdf"
    index_path = None

    try:
        content = file.file.read()

        if not content:
            raise HTTPException(400, "Uploaded PDF is empty.")

        pdf_path.write_bytes(content)

        processed_data = process_document(str(pdf_path))

        index_path = save_faiss_index(
            processed_data["index"],
            document_id
        )

        save_document(
            document_id=document_id,
            filename=file.filename,
            file_path=str(pdf_path),
            index_path=index_path,
            summary=processed_data["summary"],
            chunks=processed_data["chunks"]
        )

        return {
            "message": "PDF processed and saved successfully.",
            "document_id": document_id,
            "filename": file.filename,
            "total_chunks": len(processed_data["chunks"]),
            "summary": processed_data["summary"]
        }

    except HTTPException:
        raise

    except Exception as e:
        if pdf_path.exists():
            pdf_path.unlink()

        if index_path:
            delete_faiss_index(index_path)

        raise HTTPException(
            status_code=500,
            detail=f"PDF processing failed: {str(e)}"
        )


@app.get("/documents")
def get_documents():

    documents = get_all_documents()

    return {
        "documents": [
            {
                "document_id": doc["document_id"],
                "filename": doc["filename"]
            }
            for doc in documents
        ]
    }


@app.get("/summary/{document_id}")
def get_summary(document_id: str):

    document = get_document(document_id)

    if not document:
        raise HTTPException(404, "Document not found.")

    return {
        "document_id": document_id,
        "filename": document["filename"],
        "summary": document["summary"]
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    document = get_document(request.document_id)

    if not document:
        raise HTTPException(404, "Document not found.")

    try:
        index = load_faiss_index(document["index_path"])

        answer = ask_document_question(
            request.question,
            index,
            document["chunks"]
        )

        return {
            "document_id": request.document_id,
            "question": request.question,
            "answer": answer
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Question answering failed: {str(e)}"
        )


@app.delete("/documents/{document_id}")
def delete_document(document_id: str):

    document = get_document(document_id)

    if not document:
        raise HTTPException(404, "Document not found.")

    try:
        delete_faiss_index(document["index_path"])

        pdf_path = Path(document["file_path"])

        if pdf_path.exists():
            pdf_path.unlink()

        delete_document_record(document_id)

        return {
            "message": "Document and its stored data deleted successfully."
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Document deletion failed: {str(e)}"
        )
