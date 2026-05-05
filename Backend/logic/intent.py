# logic/intent.py
from services.llm_router import call_llm

def detect_intent(text):
    messages = [
    {
        "role": "system",
        "content": """
Classify the user intent STRICTLY into one of these:

1. refund → if user wants refund, damaged item, missing item
2. exchange → if user wants replacement or size change
3. query → only for general questions (policy, info)

IMPORTANT:
- "damaged", "broken", "not working" → refund
- "replace", "exchange" → exchange
- ONLY pure questions → query

Return ONLY one word:
refund / exchange / query
"""
    },
    {
        "role": "user",
        "content": text
    }
    ]

    result = call_llm(messages, use_case="general")

    return result.lower().strip()