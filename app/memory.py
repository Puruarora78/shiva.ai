class Conversation :
    def __init__(self, system_prompt):
        self.system_prompt = system_prompt
        self.summary = ""
        self.messages = []

    def mes_count(self):
        return len(self.messages)
    
    def set_summary(self,summary):
        self.summary = summary

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

    def get_recent_messages(self):
        return self.messages[-10:]

    def get_messages(self):
        messages = [{"role" : "system","content" : self.system_prompt}]

        if self.summary :
            messages.append({"role": "system", "content" : f"This is the summary of previous conversation use this as context ->\n {self.summary}"})

        messages.extend(self.messages)
        
        return messages