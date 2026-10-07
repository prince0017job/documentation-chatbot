from .embedding_service import create_embeddings


chunks = [
    {
        "text": "Students must maintain 75 percent attendance.",
        "page": 1
    },
    {
        "text": "The examination rules apply to all students.",
        "page": 2
    }
]


embeddings = create_embeddings(chunks)

print("Number of chunks:", len(embeddings))
print("Embedding dimensions:", embeddings.shape)