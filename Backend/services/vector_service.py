# services/vector_service.py

import logging
import os

logger = logging.getLogger(__name__)
_pc = None
_index = None


def get_index():
    global _pc, _index
    if _index is not None:
        return _index

    api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX_NAME")

    if not api_key or not index_name:
        logger.warning("Pinecone is not configured; vector search is disabled")
        _index = None
        return None

    try:
        from pinecone import Pinecone

        _pc = Pinecone(api_key=api_key)
        _index = _pc.Index(index_name)
        logger.info("Pinecone index initialized: %s", index_name)
    except Exception as exc:
        logger.exception("Failed to initialize Pinecone: %s", exc)
        _index = None

    return _index


def store_vector(id, vector, metadata=None):
    try:
        index = get_index()
        if index is None:
            return

        index.upsert([
            {
                "id": id,
                "values": vector,
                "metadata": metadata or {}
            }
        ])
    except Exception as e:
        logger.exception("Pinecone Store Error: %s", e)


def search_vector(vector, top_k=3):
    try:
        index = get_index()
        if index is None:
            return []

        result = index.query(
            vector=vector,
            top_k=top_k,
            include_metadata=True
        )
        return result["matches"]
    except Exception as e:
        logger.exception("Pinecone Search Error: %s", e)
        return []