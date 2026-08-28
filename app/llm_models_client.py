import requests
from .config import OLLAMA_BASE_URL,OLLAMA_MODEL


def generate_response(messages : list[dict] ) -> str:
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/chat",
        json = {
            "model" : OLLAMA_MODEL,
            "messages" : messages,
            "stream" : False
        },
    )
    response.raise_for_status()
    data = response.json()
    return data["message"]["content"]

