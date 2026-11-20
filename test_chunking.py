
from backend.services.chunking import split_text_into_chunks

text = """
Artificial Intelligence is a branch of computer science.
Machine Learning is a subset of Artificial Intelligence.
Deep Learning uses neural networks to learn patterns.
Natural Language Processing helps computers understand language.
"""

chunks = split_text_into_chunks(
    text,
    chunk_size=10,
    overlap=2
)

for i, chunk in enumerate(chunks):
    print(f"Chunk {i + 1}: {chunk}")
    print()
