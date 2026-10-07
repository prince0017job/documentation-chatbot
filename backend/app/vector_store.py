import json
import os
import faiss


VECTOR_FOLDER = "vector_store"


def get_user_vector_folder(user_id):
    return os.path.join(
        VECTOR_FOLDER,
        f"user_{user_id}"
    )


def save_vector_store(user_id, index, metadata):

    user_folder = get_user_vector_folder(user_id)

    os.makedirs(user_folder, exist_ok=True)

    index_file = os.path.join(
        user_folder,
        "faiss_index.bin"
    )

    metadata_file = os.path.join(
        user_folder,
        "metadata.json"
    )

    faiss.write_index(
        index,
        index_file
    )

    with open(
        metadata_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metadata,
            file,
            indent=4,
            ensure_ascii=False
        )


def load_vector_store(user_id):

    user_folder = get_user_vector_folder(user_id)

    index_file = os.path.join(
        user_folder,
        "faiss_index.bin"
    )

    metadata_file = os.path.join(
        user_folder,
        "metadata.json"
    )

    if not os.path.exists(index_file):
        return None, []

    index = faiss.read_index(
        index_file
    )

    with open(
        metadata_file,
        "r",
        encoding="utf-8"
    ) as file:

        metadata = json.load(file)

    return index, metadata