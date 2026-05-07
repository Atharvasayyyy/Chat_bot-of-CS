# services/embedding_service.py

import logging
import os

logger = logging.getLogger(__name__)

_model = None


def get_model():
    global _model
    if _model is not None:
        return _model

    model_name = os.getenv("EMBEDDING_MODEL_NAME", "intfloat/multilingual-e5-small")

    try:
        from sentence_transformers import SentenceTransformer

        _model = SentenceTransformer(model_name)
        logger.info("Embedding model loaded: %s", model_name)
    except Exception as exc:
        logger.exception("Failed to load embedding model %s: %s", model_name, exc)
        _model = None

    return _model


def get_embedding(text, is_query=True):
    """
    Generate embedding using multilingual-e5-small

    Args:
        text (str): input text
        is_query (bool): True for query, False for KB document

    Returns:
        list: embedding vector
    """
    try:
        model = get_model()
        if model is None:
            return None

        # E5 requires prefix
        prefix = "query: " if is_query else "passage: "
        embedding = model.encode(prefix + text).tolist()
        return embedding

    except Exception as exc:
        logger.exception("Embedding Error: %s", exc)
        return None