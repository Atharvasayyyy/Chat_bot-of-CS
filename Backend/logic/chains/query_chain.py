# logic/chains/query_chain.py

from logic.kb_retriever import retrieve_kb_context
from services.llm_router import call_llm

def query_flow(user_input):
    context = retrieve_kb_context(user_input)

    messages = [
        {
            "role": "system",
            "content": f"Use this context to answer:\n{context}"
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    return call_llm(messages, use_case="general")