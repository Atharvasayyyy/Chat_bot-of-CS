# services/llm_mistral_service.py
import os
import requests

def call_mistral(messages):
    try:
        url = "https://api.mistral.ai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {os.getenv('MISTRAL_API_KEY')}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "mistral-small",
            "messages": messages,
            "temperature": 0.3   # lower = safer for actions
        }

        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        print("Mistral Error:", e)
        return "Error from Mistral"