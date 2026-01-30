# StreamKar AI Support Bot 🤖

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68%2B-green)
![Gemini API](https://img.shields.io/badge/AI-Gemini%201.5%20Flash-orange)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

An intelligent, context-aware chatbot designed to assist users of **StreamKar**. Powered by Google's **Gemini API** and built with **FastAPI**, this bot answers questions regarding account management, streaming features, salary withdrawals, and technical support.

## 🚀 Features

* **Context-Aware AI:** Uses a custom knowledge base (`context.txt`) to provide accurate, specific answers about StreamKar.
* **Real-time Streaming:** Fast responses using the lightweight Gemini 2.5 Flash model.
* **Web Interface:** A clean, responsive HTML/CSS/JS chat interface similar to modern support widgets.
* **System Guardrails:** Prevents hallucinations by strictly grounding answers in the provided context.
* **Scalable Backend:** Asynchronous handling via FastAPI to support multiple concurrent users.

## 📂 Project Structure

```bash
├── main.py            # The FastAPI backend application
├── context.txt        # The knowledge base (FAQ, Rules, Policies)
├── index.html         # The frontend user interface
├── requirements.txt   # Python dependencies
└── README.md          # Documentation
