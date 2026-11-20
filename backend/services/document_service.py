
from backend.services.retrieval import (
    build_document_index,
    retrieve_relevant_chunks
)

from backend.services.groq_service import generate_response


def summarize_document(chunks):

    if not chunks:
        raise ValueError("PDF contains no readable text.")

    combined_text = "\n\n".join(chunks)

    prompt = f"""
    You are ResearchMate AI.

    Summarize this document using these headings:
    1. Document Overview
    2. Main Topics
    3. Important Concepts
    4. Key Findings
    5. Important Takeaways

    Use simple English. Preserve important facts.
    Do not invent information.

    DOCUMENT:
    {combined_text}

    SUMMARY:
    """

    return generate_response(prompt)


def process_document(pdf_path):

    index, chunks = build_document_index(pdf_path)

    summary = summarize_document(chunks)

    return {
        "index": index,
        "chunks": chunks,
        "summary": summary
    }


def ask_document_question(question, index, chunks):

    results = retrieve_relevant_chunks(
        question,
        index,
        chunks,
        top_k=3
    )

    if not results:
        return "No relevant information found in the document."

    context = "\n\n".join(
        result["text"] for result in results
    )

    prompt = f"""
    Answer using ONLY the provided document context.
    Do not invent information.
    If the answer is unavailable, say so.

    DOCUMENT CONTEXT:
    {context}

    QUESTION:
    {question}

    ANSWER:
    """

    return generate_response(prompt)
