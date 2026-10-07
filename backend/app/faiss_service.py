import faiss
import numpy as np


def create_faiss_index(embeddings):

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    index.add(embeddings)

    return index


def search_faiss(index, query_embedding, top_k=3):

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    return distances, indices
