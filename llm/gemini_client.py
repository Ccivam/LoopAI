# llm/gemini_client.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

def ask_gemini(prompt: str) -> str:
    """
    Sends the user prompt to OpenRouter (Gemini) and returns the AI response.
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "google/gemini-2.5-flash",  # double-check your OpenRouter dashboard for available models
        "messages": [
            {"role": "system", "content": "You are Loop AI, a helpful hospital network assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_output_tokens": 500
    }

    try:
        resp = requests.post(BASE_URL, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()  # raises exception for 4xx/5xx errors
        data = resp.json()
        # OpenRouter returns: data['choices'][0]['message']['content']
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print("Error calling OpenRouter:", e)
        return "I'm sorry, I am having trouble answering that right now."
