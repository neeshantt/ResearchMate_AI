import faiss
import numpy as np


def create_vector_store(embeddings):

    embeddings = np.asarray(
        embeddings,
        dtype=np.float32
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    return index





def search_similar_chunks(index, query_embedding, chunks, top_k=3):

    query_embedding = np.asarray(
        query_embedding,
        dtype=np.float32
    )

    query_embedding = query_embedding.reshape(1, -1)

    scores, indices = index.search(query_embedding, top_k)

    results = []

    for score, idx in zip(scores[0], indices[0]):

        if idx == -1:
            continue

        results.append({
            "text": chunks[idx],
            "score": float(score)
        })

    return results

