# services/vector_service.py
import os
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

def store_vector(id, vector, metadata=None):
    try:
        index.upsert([
            {
                "id": id,
                "values": vector,
                "metadata": metadata or {}
            }
        ])
    except Exception as e:
        print("Pinecone Store Error:", e)


def search_vector(vector, top_k=3):
    try:
        result = index.query(
            vector=vector,
            top_k=top_k,
            include_metadata=True
        )
        return result["matches"]
    except Exception as e:
        print("Pinecone Search Error:", e)
        return []