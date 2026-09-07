class Conversation :
    def __init__(self, system_prompt):
        self.system_prompt = system_prompt
        self.summary = ""
        self.messages = []

    def add_user_message(self,content):
        self.messages.append(
            {"role" : "user",
            "content" : content,}
        )

    def add_assistant_message(self,content):
        self.messages.append (
            {"role" : "assistant",
             "content" : content}
        )

    def get_messages(self):
        messages = [{"role" : "system","content" : self.system_prompt}]

        if self.summary :
            {"role": "system", "content" : f"Here is the messages summary ->\n {self.summary}"}

        messages.extend(self.messages)
        return messages

    def mes_count(self):
        return len(self.messages)