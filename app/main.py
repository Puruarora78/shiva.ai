from .config import PROMPT_SYSTEM
from .memory import Conversation
from .factory import create_llm_provider
from .memory_manager import Memory_Manager

conversation = Conversation(PROMPT_SYSTEM)
memory_manager = Memory_Manager(conversation)

provider = create_llm_provider()

while True:
    user_message = input(f"Enter Your Query : ")

    if user_message.lower == "exit":
        break

    conversation.add_user_message(user_message)
    answer = provider.generate(conversation.get_messages())
    conversation.add_assistant_message(answer)
    print(f"<------------------------->\n{answer}\n<------------------------->")