import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def call_groq(messages):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant", # fast + free
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        print("LLM Error:", e)
        return "LLM error"