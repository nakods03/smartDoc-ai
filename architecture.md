SmartDocs AI — System Architecture

SmartDocs AI is a lightweight, retrieval-augmented document assistant that processes PDF documents, extracts insights, and provides context-aware responses using Groq’s Llama-3.1 model.
This document explains the architecture, data flow, and design decisions behind the system.

🧩 High-Level Architecture Overview
              ┌───────────────────────────┐
              │        Streamlit UI       │
              │  (Upload, Chat, Summary)  │
              └──────────────┬────────────┘
                             │
                 User Input / PDF Upload
                             │
              ┌──────────────▼────────────┐
              │    document_loader.py     │
              │  - PDF Parsing (PyPDF2)   │
              │  - Text Extraction         │
              │  - Chunking Engine         │
              │  - Metadata Computation    │
              └──────────────┬────────────┘
                             │
                        Extracted Text
                             │
              ┌──────────────▼────────────┐
              │       chat_engine.py      │
              │  - Build contextual prompt │
              │  - Summary generation      │
              │  - Keyword extraction      │
              │  - Groq Llama-3.1 API call │
              └──────────────┬────────────┘
                             │
                     Model Response
                             │
              ┌──────────────▼────────────┐
              │       Streamlit UI        │
              │  - Chat bubbles UI        │
              │  - Summary tab            │
              │  - Insights tab           │
              │  - Search mode            │
              └───────────────────────────┘
Core Modules
1️⃣ app.py — Main Application Layer

Handles all user-facing interactions:

PDF upload UI

Sidebar navigation

Routing between Chat / Summary / Search / Insights

Rendering all output from Groq API

Responsibilities:
Function	Purpose
load_pdf()	Reads PDF and stores extracted text in session
show_chat_ui()	Renders chat-style interface
show_summary_ui()	Displays auto-generated summary
show_insights()	Shows stats like keywords, pages, word count
show_search_ui()	Searches inside chunks
2️⃣ document_loader.py — Document Processing Layer
Key Functions:
Function	Description
extract_text_from_pdf()	Converts PDF → raw text using PyPDF2
chunk_text()	Splits long text into semantic chunks
get_metadata()	Computes page count, word count, etc.

This layer is responsible for making the text structured and model-friendly.

3️⃣ chat_engine.py — AI Processing Layer

Powered by Groq Llama-3.1-8B-Instant.

Responsibilities:

Builds contextual prompts

Performs Q&A by injecting relevant chunks

Generates summaries

Extracts keywords

Ensures the model answers ONLY from the document

Key Methods:
Method	Purpose
answer_question()	Context-aware retrieval + Groq completion
generate_summary()	Summaries from full doc
extract_keywords()	Keyword extraction
⚡ Key Design Decisions
1️⃣ Why Groq Llama-3.1?

Free tier

No quota limits

Fast inference

Modern 2025 LLM architecture

Perfect for student challenge submissions

2️⃣ Why Chunking?

LLMs cannot take entire huge PDFs at once.

Chunking:

Preserves context

Prevents model hallucination

Enables precise Q&A

Makes search faster

3️⃣ Retrieval-Augmented Prompting

Each user question:

Runs keyword match

Selects only relevant chunks

Injects them into prompt

Gives factual, document-based answers

📊 Data Flow Diagram
PDF → Text Extractor → Chunker → Stored in Session  
User Query → Chunk Selector → Prompt Builder → Groq Model  
Groq Response → UI Renderer (Chat, Summary, Insights)

🧪 Model Used
Model: llama-3.1-8b-instant
Provider: Groq Cloud
Format: Chat Completions API
Features Used:

Causal inference

Instruction following

Token-efficient summaries

Fast context reasoning

🔐 Security & Key Management

.env file stores API keys locally

.env is ignored via .gitignore

No keys are committed to GitHub

Safe for public submission

🏁 Conclusion

SmartDocs AI is a clean, modular, and fast prototype demonstrating:

Document parsing

Retrieval-augmented Q&A

Multi-mode AI interface

Real-time insights

Production-style structure

This architecture is scalable and can easily expand into:

Multi-document memory

Vector database (Faiss / Chroma)

Multi-modal file support

Async processing