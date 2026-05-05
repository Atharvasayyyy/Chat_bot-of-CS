# logic/chains/refund_chain.py
from services.llm_router import call_llm

def refund_chain(user_input):
    messages = [
        {"role": "system", "content": "Handle refund carefully"},
        {"role": "user", "content": user_input}
    ]

    return call_llm(messages, use_case="refund")