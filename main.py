import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Configuration
app = FastAPI()

# Enable CORS so your frontend can talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins (simplest for initial deployment)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Knowledge Base
try:
    with open("context.txt", "r") as f:
        KNOWLEDGE = f.read()
except FileNotFoundError:
    KNOWLEDGE = "StreamKar FAQ data not found."

# Setup Gemini
# Note: In production, this key is loaded from the server's environment variables
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-3-flash')
else:
    model = None

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "StreamKar Bot is running"}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if not model:
        raise HTTPException(status_code=500, detail="API Key not configured")
    
    # System Prompting
    prompt = f"""
    You are the official Support Bot for StreamKar. 
    Use the Context below to answer the user's question.
    If the answer is not in the context, politely say you don't know and advise them to contact official support.
    
    Context: {KNOWLEDGE}
    
    User: {request.message}
    """
    
    try:
        response = await model.generate_content_async(prompt)
        return {"reply": response.text}
    except Exception as e:
        return {"reply": "I'm having trouble connecting right now. Please try again later."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
