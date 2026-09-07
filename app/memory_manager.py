from .memory import Conversation
from .llm_provider import LLMProvider

class Memory_Manager:
    def __init__(self,conversation,provider):
        self.conversaton = conversation
        self.provider = provider
        self.max_messages = 20

    def conv_count(self):
        return len(self.conversaton.messages)

    def need_summary(self):
        return self.conv_count() > self.max_messages

    def summarize_messages(self):
        return self.conversaton.messages[:-10]

    def recent_messages(self):
        return self.conversaton.messages[-10:]

    summary_prompt = ''' summarize this coversation while keeping facts and important details which might help in the convo later on '''
    def summarize_prompt (self,messages):
        return [{"role": "system",
                 "content": self.summary_prompt},
                {"role": "user",
                 "content": str(messages)} ]

    def generate_summary(self):
        messages = self.summarize_messages()
        prompt = self.summarize_prompt(messages)
        return self.provider.generate(prompt)