from .config import LLM_MODE
from .llm_provider import LLMProvider
from .Open_AI_provider import openai_provider
from .Ollama_provider import ollama_provider

def create_llm_provider() -> LLMProvider:
    if LLM_MODE == "OLLAMA":
        return ollama_provider()

    if LLM_MODE == "OpenAI":
        return openai_provider()

    raise ValueError (f'Wrong LLM Mode : {LLM_MODE}')