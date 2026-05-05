# services/llm_router.py
from .llm_service01 import call_groq
from .llm_service02 import call_mistral

def call_llm(messages, use_case="general"):
    """
    use_case:
    - general
    - refund
    - exchange
    """

    if use_case == "general":
        return call_groq(messages)

    elif use_case in ["refund", "exchange"]:
        return call_mistral(messages)

    else:
        # fallback
        return call_groq(messages)