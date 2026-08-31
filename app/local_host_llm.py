from app.config import PROMPT_SYSTEM
from app.Ollama_provider import generate_response
from app.local_host_memory import Conversation

conversation = Conversation(PROMPT_SYSTEM)

user_message = input(f"Enter Your Query : ")

conversation.add_user_message(user_message)
answer = generate_response(conversation.get_messages())
conversation.add_assistant_message(answer)
print(answer)