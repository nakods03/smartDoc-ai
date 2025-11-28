# SmartDocs AI - Architecture Documentation

## Overview

SmartDocs AI is a knowledge base agent that processes PDF documents and answers questions using GPT models.

## Architecture Components

### 1. Document Loader (`document_loader.py`)
- **Purpose**: Extract text from PDF files
- **Functionality**:
  - PDF parsing and text extraction
  - Text chunking (in-memory)
  - Metadata tracking (page numbers, chunk indices)

### 2. Chat Engine (`chat_engine.py`)
- **Purpose**: Process queries and generate responses
- **Functionality**:
  - In-memory text chunk storage
  - Relevant chunk retrieval based on queries
  - GPT API integration
  - Citation generation
  - Chat history management

### 3. Main Application (`app.py`)
- **Purpose**: Streamlit UI and orchestration
- **Functionality**:
  - File upload interface
  - Chat interface
  - Message history display
  - Citation display

## Data Flow

1. User uploads PDF → Document Loader extracts text → Chunks stored in memory
2. User asks question → Chat Engine finds relevant chunks → GPT generates response with citations
3. Response displayed with relevant excerpts and citations
4. Chat history maintained for context

## Design Decisions

- **No Vector Database**: Using simple in-memory text chunks for simplicity
- **GPT-4o-mini**: Cost-effective model for prototype
- **Streamlit**: Rapid UI development and easy cloud deployment
- **In-Memory Storage**: Suitable for single-session use

## Future Enhancements

- Vector database integration for better semantic search
- Multi-document support
- Persistent chat history
- Advanced citation formatting

