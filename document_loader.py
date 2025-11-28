import PyPDF2


def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    full_text = ""
    page_count = len(reader.pages)
    
    for page in reader.pages:
        try:
            full_text += page.extract_text() + "\n"
        except:
            continue
    
    word_count = len(full_text.split())
    
    return {
        "text": full_text,
        "page_count": page_count,
        "word_count": word_count
    }



def chunk_text(text, chunk_size=1200):
    chunks = []
    words = text.split()
    current = []

    for word in words:
        current.append(word)
        if len(current) >= chunk_size:
            chunks.append(" ".join(current))
            current = []

    if current:
        chunks.append(" ".join(current))

    return chunks
