
from backend.services.retrieval import (
    build_document_index,
    retrieve_relevant_chunks
)


# Step 1: Select PDF
pdf_path = "data/sample.pdf"


# Step 2: Build document index
index, chunks = build_document_index(pdf_path)

print("Document indexed successfully!")
print("Total chunks:", len(chunks))


# Step 3: Ask a question
query = "What are the main topics discussed in this document?"


# Step 4: Retrieve relevant chunks
results = retrieve_relevant_chunks(
    query,
    index,
    chunks,
    top_k=3
)


# Step 5: Display results
print("\nRelevant information:\n")

for i, result in enumerate(results):

    print(f"Result {i + 1}")

    print("Similarity:", result["score"])

    print("Content:", result["text"])

    print("-" * 50)
