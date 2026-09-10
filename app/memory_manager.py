from .memory import Conversation
from .llm_provider import LLMProvider

class Memory_Manager:
    def __init__(self,conversation:Conversation,provider:LLMProvider):
        self.conversation = conversation
        self.provider = provider
        self.max_messages = 20
        self.summary_index = 0

    def conv_count(self):
        return len(self.conversaton.messages)

    def need_summary(self):
        return (self.conv_count() > self.max_messages and (len(self.conversation.messages)-10) > self.summary_index)

    def summarize_messages(self):
        return self.conversaton.messages[self.summary_index : -10]

    summary_prompt = ''' this is summary we already have maintain it and summarize this coversation while keeping facts and important details which might help in the convo later on now update the already given summary with this conversation as well thank you'''
    def summarize_prompt (self,messages):
        return [{"role": "system",
                 "content": self.summary_prompt},
                {"role": "user",
                 "content": f"existing summary :\n{self.conversation.summary}\n\nnew messages :\n{messages}"} ]

    def generate_summary(self):
        messages = self.summarize_messages()
        prompt = self.summarize_prompt(messages)
        summary = self.provider.generate(prompt)
        self.conversation.set_summary(summary)
        self.summary_index = len(self.conversation.messages) - 10
        # self.conversaton.get_recent_messages()
        return summary