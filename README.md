# 🤖 StreamKar Bot: AI Support Agent

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Gemini AI](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-8E75B2?style=for-the-badge&logo=google)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

**StreamKar Bot** is an intelligent, multimodal support assistant built for the **StreamKar** platform. Unlike traditional chatbots, StreamKar Bot utilizes **Google Gemini 2.5 Flash** to "see" user issues through screenshots and **Flux AI** to purely generate creative brand assets on demand.

---

## 🚀 Key Features

### 1. 🧠 Context-Aware Support (RAG)
* **Intelligent Retrieval:** answers complex queries about StreamKar policies (PK Battles, Agency, Withdrawals) using a grounded Knowledge Base.
* **Zero Hallucinations:** Strictly adheres to the provided context (`context.txt`) to ensure accurate support.

### 2. 👁️ Vision Analysis (Multimodal)
* **Screenshot Debugging:** Users can upload screenshots of error messages or app interfaces.
* **Visual Reasoning:** The bot analyzes the image using Gemini Vision to identify the problem and suggest a fix instantly.

### 3. 🎨 Generative AI Branding
* **Flux Model Integration:** Generates high-quality, 3D neon-style avatars.
* **Smart Prompting:** Uses prompt engineering to maintain brand consistency (Official StreamKar Logo style) without needing external reference images.

---

## 🛠️ System Architecture

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **LLM Core** | `Google Gemini 2.5 Flash` | Reasoning, Chat, and Vision processing. |
| **Backend** | `FastAPI` (Python) | High-performance async API to handle requests. |
| **Image Gen** | `Pollinations.ai (Flux)` | Serverless generation of brand assets. |
| **Frontend** | `HTML5 / CSS3 / JS` | Responsive chat interface with file upload support. |
| **Database** | `Context.txt` (Flat File) | Lightweight knowledge base for RAG. |

---

### Vision Analysis
> **User:** *Uploads screenshot of login error*
>
> **KarBot:** "I see a 'Network Timeout' error in your screenshot. Please check your connection or try clearing the app cache."

### Image Generation
> **User:** "Create a logo for me."
>
> **StreamKar Bot:** *Generates a 3D Cyberpunk StreamKar themed Logo.*

---

## 💻 Installation & Setup

### Prerequisites
* Python 3.9 or higher
* Google AI Studio API Key

### 1. Clone the Repository
```bash
git clone [https://github.com/superuser303/streamkar-bot.git](https://github.com/superuser303/streamkar-bot.git)
cd streamkar-bot
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Configuration
* Create a `.env` file in the root directory and add your API key:
```bash
GEMINI_API_KEY=your_actual_api_key_here
```
### 4. Run the Server
```bash
python main.py
```
* The server will start at `http://localhost:8000` (or `0.0.0.0:8000` for deployments).

### 📂 Project Structure
```bash
streamkar-bot/
├── main.py              # Application Entry Point & API Logic
├── index.html           # Frontend Interface
├── context.txt          # Knowledge Base Source
├── requirements.txt     # Python Package List
├── logo2.png            # Static Assets
└── README.md            # Documentation
```
### 🤝 Contributing
* Contributions are welcome! Please fork the repository and submit a Pull Request.
1. Fork the Project
2. Create your Feature Branch **(`git checkout -b feature/NewFeature`)**
3. Commit your Changes **(`git commit -m 'Add some NewFeature'`)**
4. Push to the Branch **(`git push origin feature/NewFeature`)**
5. Open a Pull Request
