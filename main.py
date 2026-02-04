import os
import random
import urllib.parse
import base64
import requests 
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPICallError, RetryError
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response 
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- LOAD KNOWLEDGE BASE ---
try:
    with open("context.txt", "r") as f:
        KNOWLEDGE_BASE = f.read()
except FileNotFoundError:
    KNOWLEDGE_BASE = "Context unavailable."

# --- CONFIGURE GEMINI ---
API_KEYS = [
    os.getenv("GEMINI_API_KEY"),
    os.getenv("GEMINI_API_KEY_2") 
]

SYSTEM_PROMPT = """
You are 'StreamKar Bot', the helpful support assistant for StreamKar.

GUIDELINES:
1. Be polite but CONCISE (Max 3 sentences).
2. Use **Bold** for buttons/menus.
3. Use Bullet points for steps.
4. Answer ONLY from the Context.
5. If the user uploads an image, analyze it helpfully.

Context:
""" + KNOWLEDGE_BASE

# --- FALLBACK FUNCTION ---
async def generate_with_fallback(contents):
    """Tries to generate content using keys one by one."""
    last_error = None
    
    for i, key in enumerate(API_KEYS):
        if not key: continue 
        
        try:
            genai.configure(api_key=key)
            model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=SYSTEM_PROMPT)
            response = await model.generate_content_async(contents)
            return response
            
        except (GoogleAPICallError, RetryError, Exception) as e:
            print(f"⚠️ Key #{i+1} failed. Switching to next key... Error: {e}")
            last_error = e
            
    raise last_error or Exception("All API keys failed.")
    
# --- REQUEST MODELS ---
class ChatRequest(BaseModel):
    message: str
    image: str | None = None

# --- ENDPOINT 1: CHAT & VISION ---
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        content = []
        
        # 1. Handle Image (Vision)
        if request.image:
            # Remove header if present
            if "base64," in request.image:
                header, base64_str = request.image.split("base64,")
                # Simple MIME detection
                mime_type = "image/png" if "png" in header else "image/jpeg"
                request.image = base64_str
            else:
                mime_type = "image/jpeg" # Default

            image_data = base64.b64decode(request.image)
            image_parts = {
                "mime_type": mime_type,
                "data": image_data
            }
            content.append(image_parts)
            content.append("Analyze this image in the context of StreamKar. If it's a screenshot, explain what's happening.")

        # 2. Add Text
        content.append(request.message)

        # 3. Generate
        response = await generate_with_fallback(content)
        return {"reply": response.text}

    except Exception as e:
        print(f"Error: {e}")
        return {"reply": "I'm having trouble analyzing that. Please try again."}

# --- ENDPOINT 2: LOGO GENERATION (SECURE PROXY) ---
@app.post("/generate-logo")
async def generate_logo_endpoint():
    # 1. Get Key securely
    pollinations_key = os.getenv("POLLINATIONS_API_KEY")
    if not pollinations_key:
        print("⚠️ Warning: POLLINATIONS_API_KEY not found in .env")

    ref_image = "https://raw.githubusercontent.com/superuser303/streamkar-bot/main/logo2.png"
    
    # Define prompt
    prompt = "cyberpunk neon style, glowing purple and gold edges, 3d glossy render, futuristic, high quality, 8k resolution, Avatars of the reference image in different poses, profile pic worthy, natural look & features"  
    
    # 2. URL Encode (CRITICAL FIX for 502 Error)
    encoded_prompt = urllib.parse.quote(prompt)
    encoded_ref = urllib.parse.quote(ref_image)
    seed = random.randint(1, 99999)
    
    # 3. Construct URL
    # We add &model=flux for stability and &key= for authentication
    base_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
    params = f"?image={encoded_ref}&seed={seed}&nologo=true&model=flux"
    
    if pollinations_key:
        params += f"&key={pollinations_key}"
        
    final_url = base_url + params
    
    try:
        # 4. Fetch the image securely (Backend-to-Backend)
        print(f"Generating logo with seed {seed}...")
        response = requests.get(final_url, timeout=30) # 30s timeout
        
        # Check if Pollinations returned an error (like 502 or 403)
        if response.status_code != 200:
            print(f"Pollinations Error: {response.status_code} - {response.text}")
            return {"error": f"Pollinations API Error: {response.status_code}"}

        # 5. Return the image bytes directly
        return Response(content=response.content, media_type="image/jpeg")

    except Exception as e:
        print(f"Generation Failed: {e}")
        return {"error": "Failed to generate logo. Please try again."}

@app.get("/")
async def root():
    return {"status": "alive", "message": "StreamKar Bot is running!"}
 
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
