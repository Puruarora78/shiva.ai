from fastapi import FastAPI,HTTPException
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
    return conversations

@app.get("/conversations/{conversation_id}")
def get_conversation(conversation_id:int):
    conversation = database.get_conversation(conversation_id)
    if conversation == None:
        raise HTTPException (status_code=404 ,detail="Conversation Not Found")
    return conversation

@app.get("/conversations/{conversation_id}/messages")
def get_messages(conversation_id:int):
    conversation = database.get_conversation(conversation_id)
    if conversation == None:
        raise HTTPException(status_code=404 ,detail="Conversation Not Found")
    messages = database.get_messages(conversation_id)
    return messages

@app.post("/conversations/{conversation_id}/messages")
def send_messages(conversation_id:int,request:message_request):
    conversation_exist = database.get_conversation(conversation_id)
    if conversation_exist == None:
        raise HTTPException(status_code=404 , detail= "Conversation Does Not Exist")
    conversation = Conversation(PROMPT_SYSTEM,conversation_id)

    messages = database.get_messages(conversation_id)
    conversation.load_messages(messages)

    loaded_summary,loaded_summary_message_id = database.load_summary(conversation_id)
    conversation.set_summary(loaded_summary)
    conversation.summary_message_id = loaded_summary_message_id

    memory_Manager = Memory_Manager(conversation,provider,database)

    message_id_us = database.save_messages(conversation_id,"user",request.message)
    message = conversation.add_user_message(request.message,message_id_us)

    try:
        answer = provider.generate(conversation.get_messages())
    except RuntimeError as e :
        database.delete_message(message_id_us)
        conversation.messages.pop()
        raise HTTPException(status_code=500,detail=f"Error Occured During Generating Response : {e} ")

    message_id_as = database.save_messages(conversation_id,"assistant",answer)
    response = conversation.add_assistant_message(answer,message_id_as)

    if memory_Manager.need_summary():
        memory_Manager.generate_summary()

    return answer
    