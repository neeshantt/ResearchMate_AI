
from backend.database import (
    initialize_database,
    save_document,
    get_document,
    get_all_documents,
    delete_document
)

initialize_database()

# Insert test document
save_document(
    document_id="test-123",
    filename="sample.pdf",
    file_path="data/uploads/sample.pdf",
    index_path="data/indexes/test-123.faiss",
    summary="This is a test document."
)

# Retrieve one document
print("\nSingle Document:")
print(get_document("test-123"))

# Retrieve all documents
print("\nAll Documents:")
print(get_all_documents())

# Delete test document
print("\nDeleting Test Document:")
print(delete_document("test-123"))

# Verify deletion
print("\nAfter Deletion:")
print(get_document("test-123"))
