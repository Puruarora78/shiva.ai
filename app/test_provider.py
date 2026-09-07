from app.config import PROMPT_SYSTEM
from app.memory import Conversation


conversation = Conversation(PROMPT_SYSTEM)

conversation.add_user_message("My name is Puru.")
conversation.add_assistant_message("Nice to meet you!")

conversation.add_user_message("I am learning Python.")

print(conversation.get_messages())
print("Message count:", conversation.mes_count())