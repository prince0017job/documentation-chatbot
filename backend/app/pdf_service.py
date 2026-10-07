from pypdf import PdfReader


def extract_pages_from_pdf(file_path):
    reader = PdfReader(file_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        page_text = page.extract_text()

        if page_text:
            pages.append(
                (page_number, page_text)
            )

    return pages