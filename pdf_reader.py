import fitz

def extract_text_by_pages(pdf_file_bytes):
    doc = fitz.open(stream=pdf_file_bytes, filetype="pdf")
    pages_data = {}
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        pages_data[page_num + 1] = text
    return pages_data
