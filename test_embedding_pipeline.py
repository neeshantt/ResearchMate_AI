
from backend.pdf_loader import extract_text_from_pdf

from backend.services.chunking import split_text_into_chunks

from backend.services.embeddings import generate_embeddings


pdf_path = "data/sample.pdf"

# Step 1: Extract PDF text
text = extract_text_from_pdf(pdf_path)

# Step 2: Divide text into chunks
chunks = split_text_into_chunks(text)

# Step 3: Generate embeddings
embeddings = generate_embeddings(chunks)

print("Total chunks:", len(chunks))

print("Embedding shape:", embeddings.shape)
