from .memory import Conversation
from .llm_provider import LLMProvider
from .database import Database

class Memory_Manager:
    def __init__(self,conversation:Conversation,provider:LLMProvider,database: Database):
        self.conversation = conversation
        self.provider = provider
        self.database = database
        self.max_messages = 20
        self.summary_interval = 10

    def conv_count(self):
        return len(self.conversation.messages)
        
    def need_summary(self):

        if self.conv_count() <= self.max_messages:
            return False
        
        end = len(self.conversation.messages) - 10
        start = 0
        for i,message in enumerate(self.conversation.messages):
            if message["id"] == self.conversation.summary_message_id:
                start = i + 1
                break
        summarize_count = end -start
        if summarize_count < self.summary_interval:
            return False
        if summarize_count %2 != 0:
            return False
        return True

    def summarizing_messages(self):
        end = len(self.conversation.messages) -10
        start = 0
        for i,message in enumerate(self.conversation.messages):
            if message["id"] == self.conversation.messages:
                start = i + 1
                break
        if (end - start) %2 != 0:
            end -= 1
        return self.conversation.messages[start : end]

    summary_prompt = '''i am providing chat summary we already had upadet it with the new messages while keeping important facts and information or any query i asked dont keep unneccesary talk , dont invent new information ,if the existing summary is empty then create a new summary with new messages and only provide updated summary'''
    def summarize_prompt (self,messages):
        return [{"role": "system",
                 "content": self.summary_prompt},
                {"role": "user",
                 "content": f"existing summary :\n{self.conversation.summary}\n\nnew messages :\n{messages}"}]

    def generate_summary(self):
        messages = self.summarizing_messages()
        if not messages:
            return self.conversation.summary
        prompt = self.summarize_prompt(messages)
        summary = self.provider.generate(prompt)
        summary_message_id = messages[-1]["id"]
        self.conversation.summary_message_id = summary_message_id
        self.conversation.set_summary(summary)
        self.database.save_summary(self.conversation.conversation_id,summary,summary_message_id)
        # self.conversaton.get_recent_messages()
        return summary