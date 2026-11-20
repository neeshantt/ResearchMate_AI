
import numpy as np
import faiss

from backend.services.persistent_store import (
    save_faiss_index,
    load_faiss_index,
    delete_faiss_index
)

# Create a sample FAISS index
dimension = 384

index = faiss.IndexFlatIP(dimension)

# Generate sample normalized vectors
vectors = np.random.random((5, dimension)).astype("float32")

faiss.normalize_L2(vectors)

# Add vectors
index.add(vectors)

print("Original index size:", index.ntotal)

# Save index
index_path = save_faiss_index(index, "test-document")

print("Index saved:", index_path)

# Load index
loaded_index = load_faiss_index(index_path)

print("Loaded index size:", loaded_index.ntotal)

# Verify
assert loaded_index.ntotal == index.ntotal

print("FAISS persistence test successful!")

# Clean up test index
delete_faiss_index(index_path)

print("Test index deleted successfully!")