import os
import logging
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

# 1. Setup Logging & Environment
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

app = FastAPI()

# 2. CORS Middleware (Crucial for connecting Frontend to Backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Load Knowledge Base
try:
    with open("context.txt", "r") as f:
        KNOWLEDGE_BASE = f.read()
except FileNotFoundError:
    logger.error("context.txt not found!")
    KNOWLEDGE_BASE = "Context unavailable."

# 4. Configure Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    logger.warning("GEMINI_API_KEY not found in environment variables.")
    model = None
else:
    genai.configure(api_key=API_KEY)
    
    # --- THIS IS THE UPDATED PERSONA ---
    # We use a system instruction to force "Polite but Concise" answers.
    model = genai.GenerativeModel(
        'gemini-2.5-flash',
        system_instruction="""
        You are 'StreamKarBot', the helpful and polite support assistant for StreamKar.
        
        YOUR STYLE GUIDE:
        1. Tone: Warm, polite, and professional (Use phrases like "I can help with that", "Please try").
        2. Format Guidelines (MANDATORY):
           - Use **Bold** for all button names, menu items, and links (e.g., Go to **Settings**).
           - Use Bullet points for instructions with multiple steps.
           - Keep paragraphs short (maximum 2 sentences).
        3. Content Rule: Answer ONLY based on the provided Context. If you don't know, politely say so.
        
        Example Interaction:
        User: "How do I fix audio lag?"
        You: "I can help with that! Audio lag is usually caused by internet speed. Please try these steps:
        * Ensure your upload speed is at least **5Mbps**.
        * Go to **Profile > Settings** and tap **Clear Cache**.
        * Restart the app."
        
        Context Data:
        """ + KNOWLEDGE_BASE
    )

# 5. Data Model
class ChatRequest(BaseModel):
    message: str

# 6. Routes
@app.get("/")
def home():
    return {"status": "StreamKar Bot is running"}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if not model:
        raise HTTPException(status_code=500, detail="System Error: API Key not configured")
    
    try:
        # We append the user's message to the chat history
        prompt = f"User Question: {request.message}"
        
        response = await model.generate_content_async(prompt)
        return {"reply": response.text}
    
    except Exception as e:
        logger.error(f"Generation Error: {e}")
        return {"reply": "I'm having trouble connecting right now. Please try again in a moment."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
