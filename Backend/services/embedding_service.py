# services/embedding_service.py

from sentence_transformers import SentenceTransformer

# Load model once (global)
model = SentenceTransformer("intfloat/multilingual-e5-small")


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
        # 🔥 IMPORTANT: E5 requires prefix
        prefix = "query: " if is_query else "passage: "

        embedding = model.encode(prefix + text).tolist()

        return embedding

    except Exception as e:
        print("🔥 Embedding Error:", e)
        return None