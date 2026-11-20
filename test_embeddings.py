
from backend.services.embeddings import generate_embeddings

chunks = [
    "Artificial Intelligence is a branch of computer science.",
    "Machine Learning is a subset of Artificial Intelligence.",
    "The weather is sunny today."
]

embeddings = generate_embeddings(chunks)

print("Embeddings shape:", embeddings.shape)

print("\nFirst embedding:")
print(embeddings[0])

print("\nNumber of chunks:", len(chunks))
