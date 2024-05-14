from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from openai import AzureOpenAI
from fastapi.responses import StreamingResponse
import google.generativeai as genai

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_streamed_ai_response(response):
    for chunk in response: 
        words = chunk.text.split()
        for word in words:
            yield word+ " "

class Message(BaseModel):
    role: str
    content: str

@app.post("/message")
async def send_message(messages: List[Message]):
    genai.configure(api_key="AIzaSyDdHhOkg_LMpg4uikLlX6qkvi-HhWC4swI")
    model = genai.GenerativeModel(model_name='gemini-1.5-pro-latest',system_instruction="You are a super-intelligent AI assistant. Assist the user in any way you can.")
    chat_messages=[]
    for message in messages:
       chat_messages.append({'role': message.role, 'parts': [message.content]})
    response = model.generate_content(chat_messages, stream=True)
    return StreamingResponse(get_streamed_ai_response(response), media_type='text/event-stream')


""" #model = genai.GenerativeModel(model_name='gemini-pro',system_instruction="You are a super-intelligent AI assistant. Assist the user in any way you can.")
    #msgs=[message.dict() for message in messages],
    #input_string = " ".join([message.content for message in messages])
  const chat = model.startChat({
    history: [
      {
        role: "user",
        parts: [{ text: "Hello, I have 2 dogs in my house." }],
      },
      {
        role: "model",
        parts: [{ text: "Great to meet you. What would you like to know?" }],
      },
    ],
    generationConfig: {
      maxOutputTokens: 100,
    },
  });

  const msg = "How many paws are in my house?";

  const result = await chat.sendMessage(msg);



model = GenerativeModel('gemini-pro')
chat = model.start_chat(history=conversation_history)

# Now, you can continue the conversation by sending additional messages
# The SDK will manage the conversation history based on the messages you send
response = chat.send_message("What's the weather like today?", stream=True)
"""