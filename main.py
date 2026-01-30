import os
import logging
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import base64
import io
from PIL import Image
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
        You are 'StreamKar Bot', the helpful and polite support assistant for StreamKar.
        
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

# Update the Request Model to accept an optional image
class ChatRequest(BaseModel):
    message: str
    image: str | None = None  # Base64 encoded image string

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if not model:
        raise HTTPException(status_code=500, detail="API Key Missing")
    
    try:
        # Prepare the content for Gemini
        content = []
        
        # 1. Handle Image if provided
        if request.image:
            # Clean the base64 string (remove "data:image/png;base64," prefix)
            if "base64," in request.image:
                request.image = request.image.split("base64,")[1]
            
            # Decode image
            image_data = base64.b64decode(request.image)
            image_parts = {
                "mime_type": "image/jpeg", # defaulting to jpeg for simplicity
                "data": image_data
            }
            content.append(image_parts)
            
            # Add a specific prompt for images
            content.append("User has uploaded this image. Analyze it in the context of StreamKar support. If it's an error, explain the fix. If it's a profile, explain the features visible.")

        # 2. Add User Text
        content.append(request.message)

        # 3. Generate Response
        response = await model.generate_content_async(content)
        return {"reply": response.text}

    except Exception as e:
        print(f"Error: {e}")
        return {"reply": "I'm having trouble analyzing that image. Please try again."}
        
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
