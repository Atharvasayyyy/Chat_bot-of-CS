# # logic/kb_retriever.py

from services.embedding_service import get_embedding
from services.vector_service import search_vector

def retrieve_kb_context(query):
    print("🔎 QUERY:", query)

    vector = get_embedding(query)
    print("🧠 EMBEDDING LENGTH:", len(vector) if vector else "None")

    results = search_vector(vector)
    print("📊 RAW VECTOR RESULTS:", results)

    context = ""

    for r in results:
        print("👉 MATCH:", r)
        context += r["metadata"].get("text", "") + "\n"

    print("📚 FINAL CONTEXT:", context)

    return context