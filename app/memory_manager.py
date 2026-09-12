from .memory import Conversation
from .llm_provider import LLMProvider

class Memory_Manager:
    def __init__(self,conversation:Conversation,provider:LLMProvider):
        self.conversation = conversation
        self.provider = provider
        self.max_messages = 20
        self.summary_index = 0
        self.summary_interval = 10

    def conv_count(self):
        return len(self.conversation.messages)
        
    def need_summary(self):
        any_summ = len(self.conversation.messages) - 10

        if any_summ <= self.summary_index:
            print("false1")
            return False
        if (any_summ - self.summary_index) %2 != 0:
            print("false2")
            return False
        if (any_summ - self.summary_index) < self.summary_interval :
            print("false3")
            return False
        return self.conv_count() > self.max_messages

    def summarizing_messages(self):
        mess = self.conversation.messages[self.summary_index : -10]
        mess_len = len(mess)
        if mess_len %2 != 0:
            mess -= 1
        return self.conversation.messages[self.summary_index:mess_len]

    summary_prompt = '''i am providing chat summary we already had upadet it with the new messages while keeping important facts and information or any query i asked dont keep unneccesary talk , dont invent new information ,if the existing summary is empty then create a new summary with new messages and only provide updated summary'''
    def summarize_prompt (self,messages):
        return [{"role": "system",
                 "content": self.summary_prompt},
                {"role": "user",
                 "content": f"existing summary :\n{self.conversation.summary}\n\nnew messages :\n{messages}"}]

    def generate_summary(self):
        messages = self.summarizing_messages()
        prompt = self.summarize_prompt(messages)
        summary = self.provider.generate(prompt)
        self.conversation.set_summary(summary)
        self.summary_index = len(self.conversation.messages) - 10
        # self.conversaton.get_recent_messages()
        return summary