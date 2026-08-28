from .config import PROMPT_SYSTEM
from .memory import Conversation

conversation = Conversation(PROMPT_SYSTEM)

conversation.add_user_message("its a test")

conversation.add_assistant_message("okay then")

conversation.add_user_message("test complete")

print(conversation.get_messages())