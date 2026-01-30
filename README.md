# StreamKar AI Support Bot 🤖

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68%2B-green)
![Gemini API](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-orange)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

## 📖 About The Project

The **StreamKar AI Support Bot** is an intelligent conversational agent designed to automate customer support for [StreamKar](https://www.streamkar.com). Built to assist new and existing users, this bot instantly answers frequently asked questions regarding:

* **Account Management:** Sign-up, password resets, and profile updates.
* **Streaming Mechanics:** How to start a broadcast, PK battles, and Multi-guest features.
* **Economy:** Explanations of Beans, Gems, and salary withdrawal processes.
* **Troubleshooting:** Common fixes for audio lag, login errors, and app freezes.

### 💡 Why this exists?
StreamKar has a vast ecosystem of features that can be overwhelming for new users. This project leverages **Google's Gemini 1.5 Flash** model with a **RAG (Retrieval-Augmented Generation)** architecture to provide accurate, context-grounded answers 24/7, reducing the load on human support teams.

### ⚙️ How it works
1.  **User Input:** The user asks a question via the web interface.
2.  **Context Retrieval:** The backend retrieves relevant policy and FAQ data from a structured knowledge base (`context.txt`).
3.  **AI Processing:** The Gemini API processes the user's query along with the retrieved context to generate a helpful, human-like response.
4.  **Guardrails:** System instructions ensure the bot stays on topic and strictly adheres to StreamKar's official policies.
