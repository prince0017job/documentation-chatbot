from .chunk_service import chunk_text


text = """
This is a sample document.
It contains information about college rules.
Students must maintain attendance.
Students must follow examination regulations.
The college also has placement guidelines.
"""


chunks = chunk_text(text, chunk_size=10, overlap=2)


for i, chunk in enumerate(chunks):
    print(f"Chunk {i + 1}:")
    print(chunk)
    print()