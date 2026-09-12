import requests
from .config import OLLAMA_BASE_URL,OLLAMA_MODEL
from .llm_provider import LLMProvider

class ollama_provider(LLMProvider):
    try:
        def generate(self,messages : list[dict] ) -> str:
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
    except requests.RequestException as e:
        raise RuntimeError(f"Could not connect to Ollama : {e}")

