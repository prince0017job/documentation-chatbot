import numpy as np

from .embedding_service import create_embeddings
from .faiss_service import create_faiss_index, search_faiss


chunks = [
    {
        "text": "Students must maintain 75 percent attendance.",
        "page": 1
    },
    {
        "text": "The examination rules apply to all students.",
        "page": 2
    },
    {
        "text": "Students can participate in campus placement activities.",
        "page": 3
    }
]


# Create embeddings for the chunks
embeddings = create_embeddings(chunks)

print("Embeddings shape:", embeddings.shape)


# Create FAISS index
index = create_faiss_index(embeddings)

print("Number of vectors in FAISS:", index.ntotal)


# Create embedding for the question
question = [
    {
        "text": "What is the attendance requirement?",
        "page": 0
    }
]

question_embedding = create_embeddings(question)


# Search FAISS
distances, indices = search_faiss(
    index,
    question_embedding,
    top_k=2
)


print("Search results:")

for i in range(len(indices[0])):
    result_index = indices[0][i]

    print(
        "Chunk:",
        result_index,
        "| Distance:",
        distances[0][i]
    )

    print(
        "Text:",
        chunks[result_index]["text"]
    )