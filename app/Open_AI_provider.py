from openai import OpenAI
from .config import OPEN_AI_MODEL,OPENAI_API_KEY
from .llm_provider import LLMProvider

class openai_provider(LLMProvider):

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def generate(self, messages : list[dict]) -> str :
        response = self.client.responses.create(
            model = OPEN_AI_MODEL,
            input = messages
        )
        return response.output_text