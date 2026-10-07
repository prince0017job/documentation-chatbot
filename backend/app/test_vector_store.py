import numpy as np

from .embedding_service import create_embeddings
from .faiss_service import create_faiss_index
from .vector_store import save_vector_store, load_vector_store


chunks = [
    {
        "text": "Students must maintain 75 percent attendance.",
        "page": 1,
        "filename": "college_rules.pdf",
        "document_id": 1
    },
    {
        "text": "Students must follow examination regulations.",
        "page": 2,
        "filename": "college_rules.pdf",
        "document_id": 1
    }
]


# Create embeddings
embeddings = create_embeddings(chunks)

# Create FAISS index
index = create_faiss_index(embeddings)

# Save index and metadata
save_vector_store(index, chunks)

print("Vector store saved successfully!")


# Load it again
loaded_index, metadata = load_vector_store()

print("Loaded vectors:", loaded_index.ntotal)
print("Loaded metadata:", len(metadata))

print("First metadata:")
print(metadata[0])