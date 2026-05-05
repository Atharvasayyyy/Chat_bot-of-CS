# logic/kb_pipeline.py
from services.embedding_service import get_embedding
from services.vector_service import store_vector

def ingest_text(text, doc_id):
    embedding = get_embedding(text)
    store_vector(doc_id, embedding, {"text": text})


def ingest_url(url):
    import requests
    html = requests.get(url).text
    ingest_text(html, url)


def ingest_pdf(file, doc_id):
    from PyPDF2 import PdfReader

    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        text += page.extract_text()

    ingest_text(text, doc_id)