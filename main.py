import os
import random
import urllib.parse
import base64
import time
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

# Imports for Vision Processing
from PIL import Image
import io

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Knowledge Base
try:
    with open("context.txt", "r") as f:
        KNOWLEDGE_BASE = f.read()
except FileNotFoundError:
    KNOWLEDGE_BASE = "Context unavailable."

# Configure Gemini
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(
        'gemini-2.5-flash',
        system_instruction="""
        You are 'StreamKar Bot', the helpful support assistant for StreamKar.
        
        GUIDELINES:
        1. Be polite but CONCISE (Max 3 sentences).
        2. Use **Bold** for buttons/menus.
        3. Use Bullet points for steps.
        4. Answer ONLY from the Context.
        5. If the user uploads an image, analyze it helpfully.
        
        Context:
        """ + KNOWLEDGE_BASE
    )
else:
    model = None

# --- REQUEST MODELS ---
class ChatRequest(BaseModel):
    message: str
    image: str | None = None  # Accepts Base64 string

# --- ENDPOINT 1: CHAT & VISION ---
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if not model:
        raise HTTPException(status_code=500, detail="API Key Missing")
    
    try:
        content = []
        
        # 1. Handle Image (Vision)
        if request.image:
            # Clean base64 string
            if "base64," in request.image:
                request.image = request.image.split("base64,")[1]
            
            # Decode and prepare for Gemini
            image_data = base64.b64decode(request.image)
            image_parts = {
                "mime_type": "image/jpeg",
                "data": image_data
            }
            content.append(image_parts)
            content.append("Analyze this image in the context of StreamKar. If it's a screenshot, explain what's happening.")

        # 2. Add Text
        content.append(request.message)

        # 3. Generate
        response = await model.generate_content_async(content)
        return {"reply": response.text}

    except Exception as e:
        print(f"Error: {e}")
        return {"reply": "I'm having trouble analyzing that. Please try again."}

@app.post("/generate-logo")
async def generate_logo_endpoint():
    # 1. THE REAL WORKING REFERENCE (Google's High-Res Icon API)
    # This grabs the official StreamKar logo dynamically
    ref_image = "https://raw.githubusercontent.com/superuser303/streamkar-bot/refs/heads/main/images.jpeg"
    # 2. The Prompt (Describes the STYLE, while the image provides the SHAPE)
    prompt = "cyberpunk neon style, glowing purple and gold edges, 3d glossy render, futuristic, high quality, 8k resolution"
    
    # 3. Random Seed
    seed = random.randint(1, 99999)
    
    # 4. Construct URL
    encoded_ref = urllib.parse.quote(ref_image)
    final_url = f"https://image.pollinations.ai/prompt/{prompt}?image={encoded_ref}&seed={seed}&nologo=true"
    
    return {"image_url": final_url}
            
    return {"error": "Model took too long to load. Please try again."}
