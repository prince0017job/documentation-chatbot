def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()

    chunks = []

    start = 0

    while start < len(words):
        end = start + chunk_size

        chunk = " ".join(words[start:end])

        chunks.append(chunk)

        start = end - overlap

    return chunks


def chunk_pdf_pages(pages, chunk_size=500, overlap=50):
    chunks = []

    for page_number, page_text in pages:

        words = page_text.split()

        start = 0

        while start < len(words):

            end = start + chunk_size

            chunk = " ".join(words[start:end])

            chunks.append({
                "text": chunk,
                "page": page_number
            })

            start = end - overlap

    return chunks