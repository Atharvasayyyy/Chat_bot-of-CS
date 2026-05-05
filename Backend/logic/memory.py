# logic/memory.py

conversation_store = {}

def get_memory(user_id):
    if user_id not in conversation_store:
        conversation_store[user_id] = []
    return conversation_store[user_id]

def add_to_memory(user_id, role, content):
    conversation_store[user_id].append({
        "role": role,
        "content": content
    })

def get_last_messages(user_id, limit=10):
    return get_memory(user_id)[-limit:]