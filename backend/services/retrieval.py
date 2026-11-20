
from backend.pdf_loader import extract_text_from_pdf

from backend.services.chunking import split_text_into_chunks

from backend.services.embeddings import generate_embeddings

from backend.services.vector_store import (
    create_vector_store,
    search_similar_chunks
)


def build_document_index(pdf_path):

    # Step 1: Extract text from PDF
    text = extract_text_from_pdf(pdf_path)

    # Step 2: Split extracted text into chunks
    chunks = split_text_into_chunks(text)

    # Step 3: Convert chunks into embeddings
    embeddings = generate_embeddings(chunks)

    # Step 4: Store embeddings in FAISS
    index = create_vector_store(embeddings)

    return index, chunks


def retrieve_relevant_chunks(query, index, chunks, top_k=3):

    # Step 1: Convert user question into an embedding
    query_embedding = generate_embeddings([query])

    # Step 2: Search for similar chunks
    results = search_similar_chunks(
        index,
        query_embedding,
        chunks,
        top_k
    )

    return results
