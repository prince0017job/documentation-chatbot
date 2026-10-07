from .embedding_service import model
from .vector_store import load_vector_store


def search_documents(user_id, question, top_k=3):

    index, metadata = load_vector_store(user_id)

    if index is None:
        return []

    query_embedding = model.encode(
        [question],
        convert_to_numpy=True
    )

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for distance, index_position in zip(
        distances[0],
        indices[0]
    ):

        if index_position == -1:
            continue

        result = metadata[index_position].copy()

        result["distance"] = float(distance)

        results.append(result)

    return results