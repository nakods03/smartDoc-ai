SmartDocs AI — Intelligent Document Assistant

A lightweight, fast, and efficient AI-powered document assistant that extracts insights, summarizes PDFs, and provides context-aware question answering — built using Streamlit, Groq LLMs, and Python.

🚀 Features
📤 Document Upload

Upload PDFs of any size

Automatically extracts text and metadata (page count, word count)

🔍 Intelligent Parsing & Chunking

Splits documents into optimized chunks

Enables fast contextual search and retrieval

💬 Smart Chat (Context-Aware Q&A)

Ask any question from the document — the agent responds strictly based on document content, using:

Llama-3.1-8B-Instant (Groq)

Retrieval-enhanced context

Clean, structured responses

📝 Auto-Summary Engine

Generates a multi-paragraph summary

Rewrites summary on demand

Handles long documents efficiently

🔎 Document Search

Search ANY keyword/phrase inside your uploaded PDF:

Highlighted matches

Chunk-based retrieval

Instant response

📊 Insights Panel

Automatically displays:

Total pages

Word count

Chunk count

Estimated reading time

Auto-extracted keywords

🎨 Modern UI

Sidebar navigation

Clean dark theme

Chat-style message bubbles

Smooth and responsive layout

🧠 Tech Stack
Frontend & App

Streamlit

Custom CSS styling

Python 3.11 (virtual environment)

Backend / AI

Groq LLM API

Model: llama-3.1-8b-instant

Retrieval-augmented prompting

Chunked context injection

Document Processing

PyPDF2

Custom chunking strategy

Regex-based search

🧩 Project Structure
smartdocs/
│── app.py                 # Main Streamlit app (UI + Navigation)
│── chat_engine.py         # AI backend (Groq-based Q&A, summary, keywords)
│── document_loader.py     # PDF parsing, metadata extraction, chunking
│── architecture.md        # System architecture (high-level overview)
│── requirements.txt       # Dependencies
│── .gitignore             # Prevents env + keys from pushing
└── README.md              # Project documentation

🔧 Setup Instructions
1️⃣ Clone the Repository
git clone https://github.com/nakods03/smartDoc-ai
cd smartDoc-ai

2️⃣ Create Virtual Environment
python3.11 -m venv venv
source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Add Your API Key

Create a .env file:

GROQ_API_KEY=your_key_here

5️⃣ Run the App
streamlit run app.py

🎯 Why This Project Matters

This project demonstrates:

Real-world AI integration

Complete end-to-end product design

Strong understanding of LLM prompting

Structured architecture

Clean, scalable code

Ability to build production-style prototypes FAST

Perfect for AI engineering, software roles, and internship selection demos.