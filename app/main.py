from .config import PROMPT_SYSTEM
from .memory import Conversation
from .factory import create_llm_provider
from .memory_manager import Memory_Manager
from .database import Database

database = Database()

# create empty tables if new db is created
database.create_tables()
choose_conv = input("Write 'new' if you want to start a new chat or 'load' for using existing conversation : ")
if choose_conv.lower() == "new":
    conversation_id = database.create_conversation()
    conversation = Conversation(PROMPT_SYSTEM,conversation_id) 

elif choose_conv.lower() == "load":
    conversations = database.get_all_conversations()

    for i in conversations:
        print(i)
    loaded_conversation_id = int(input("Enter Conversation ID : "))

    conversation = Conversation(PROMPT_SYSTEM,loaded_conversation_id) 

    messages = database.get_messages(loaded_conversation_id)
    conversation.load_messages(messages)

    loaded_summary = database.load_summary(loaded_conversation_id)
    conversation.set_summary(loaded_summary)

else :
    print("Please Enter Correct Value")
    exit()

provider = create_llm_provider()

memory_manager = Memory_Manager(conversation,provider,database)

while True:
    user_message = input(f"Enter Your Query : ")

    if user_message.lower() == "exit":
        break
    conversation.add_user_message(user_message)
    database.save_messages(conversation.conversation_id,"user",user_message)

    try:
        answer = provider.generate(conversation.get_messages())
    except RuntimeError as e:
         conversation.messages.pop()
         print(f"Error Occured During Generating Response : {e}")
         continue
    
    conversation.add_assistant_message(answer)
    database.save_messages(conversation.conversation_id,"assistant",answer)
    if memory_manager.need_summary() :
        input("press enter for summary :")
        try:
            memory_manager.generate_summary()
        except RuntimeError as e :
            print(f"Error Occured During Generating Summary : {e}")
    print(f"<------------------------->\n{answer}\n<------------------------->")
    print(len(conversation.messages))
    print (conversation_id)
    convo = database.get_messages(19)

    print (convo)
    print (conversation.messages)