from backend.services.embeddings import generate_embeddings

from backend.services.vector_store import (
    create_vector_store,
    search_similar_chunks
)


chunks = [
    "Artificial Intelligence is a branch of computer science.",

    "Machine Learning allows computers to learn from data.",

    "Cricket is a popular sport in India.",

    "Deep Learning uses neural networks to learn complex patterns."
]


# Step 1: Generate document embeddings
embeddings = generate_embeddings(chunks)


# Step 2: Create FAISS index
index = create_vector_store(embeddings)


# Step 3: User question
query = "What is machine learning?"


# Step 4: Generate query embedding
query_embedding = generate_embeddings([query])


# Step 5: Search relevant chunks
results = search_similar_chunks(
    index,
    query_embedding,
    chunks,
    top_k=3
)


# Step 6: Display results
for result in results:

    print("Similarity:", result["score"])

    print("Text:", result["text"])

    print("-" * 50)
