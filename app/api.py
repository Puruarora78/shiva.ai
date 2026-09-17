from fastapi import FastAPI
from pydantic import BaseModel
from .memory import Conversation
from .database import Database
from .memory_manager import Memory_Manager
from .factory import create_llm_provider
from .config import PROMPT_SYSTEM

app = FastAPI()

database = Database()
database.create_tables()

provider = create_llm_provider()

class message_request(BaseModel):
    message : str

@app.get("/")
def Homepage():
    return("Welcome To Shiva AI")

@app.post("/conversations")
def create_conversation():
    conversation_id = database.create_conversation()
    return(f"conversation id : {conversation_id}")

@app.get("/conversations")
def get_conversations():
    conversations = database.get_all_conversations()
    return (f"conversations : {conversations}")

@app.get("/conversations/{conversation_id}")
def get_conversation(conversation_id:int):
    Convo = database.get_conversation(conversation_id)
    return Convo

@app.get("/conversations/{conversation_id}/messages")
def get_messages(conversation_id):
    messages = database.get_messages(conversation_id)
    return messages

@app.post("/conversations/{conversation_id}/messages")
def send_messages(conversation_id,request:message_request):
    conversation = Conversation(PROMPT_SYSTEM,conversation_id)

    messages = database.get_messages(conversation_id)
    conversation.load_messages(messages)

    summary = database.load_summary(conversation_id)
    conversation.set_summary(summary)

    memory_Manager = Memory_Manager(conversation,provider,database)

    if conversation.summary :
        memory_Manager.summary_index = max(0,len(conversation.messages)-10)

    message = conversation.add_user_message(request.message)
    database.save_messages(conversation_id,"user",request.message)

    answer = provider.generate(conversation.get_messages())

    response = conversation.add_assistant_message(answer)
    database.save_messages(conversation_id,"assistant",answer)

    if memory_Manager.need_summary():
        memory_Manager.generate_summary()

    return f"Response : {response}"
    

# @app.post("/conversations/{conversation_id}/summary")
# def save_summary(conversation_id,summary):
#     save_summary = database.save_summary(conversation_id,summary)
#     return (f"summary saved : {summary}")

# @app.get("/conversations/{conversation_id}/summary")
# def get_summary(conversation_id):
#     summary = database.load_summary(conversation_id)
#     return (f"summary : {summary}")