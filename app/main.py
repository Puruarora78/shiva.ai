from .config import PROMPT_SYSTEM
from .memory import Conversation
from .factory import create_llm_provider
from .memory_manager import Memory_Manager

conversation = Conversation(PROMPT_SYSTEM)
provider = create_llm_provider()

memory_manager = Memory_Manager(conversation,provider)

while True:
    user_message = input(f"Enter Your Query : ")

    if user_message.lower() == "exit":
        break
    conversation.add_user_message(user_message)

    try:
        answer = provider.generate(conversation.get_messages())
    except RuntimeError as e:
         conversation.messages.pop()
         print(f"Error Occured During Generating Response : {e}")
         continue
    
    conversation.add_assistant_message(answer)
    if memory_manager.need_summary() :
        input("press enter for summary :")
        try:
            memory_manager.generate_summary()
        except RuntimeError as e :
            print(f"Error Occured During Generating Summary : {e}")
    print(f"<------------------------->\n{answer}\n<------------------------->")
    print(len(conversation.messages))
    print(conversation.summary)