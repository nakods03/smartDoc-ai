# SmartDocs AI - Knowledge Base Agent

A 2-hour prototype AI agent that allows users to upload PDFs and ask questions about their content.

## Features

- 📄 PDF upload and text extraction
- 🤖 GPT-powered question answering
- 💬 Chat interface with memory
- 📝 Citations and relevant text excerpts
- 🎨 Clean Streamlit UI
- ☁️ Deployable on Streamlit Cloud

## Tech Stack

- Python 3.8+
- Streamlit
- OpenAI (GPT-4o-mini or GPT-4.1-mini)
- In-memory text chunks (no vector database)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
export OPENAI_API_KEY=your_api_key_here
```

3. Run the application:
```bash
streamlit run app.py
```

## Project Structure

- `app.py` - Main Streamlit application
- `document_loader.py` - PDF processing and text extraction
- `chat_engine.py` - GPT integration and chat logic
- `requirements.txt` - Python dependencies
- `architecture.md` - Architecture documentation

## TODO

- [ ] Implement PDF text extraction
- [ ] Build Streamlit UI
- [ ] Integrate OpenAI GPT API
- [ ] Add chat memory functionality
- [ ] Implement citation system
- [ ] Test and deploy to Streamlit Cloud

