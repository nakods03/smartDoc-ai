import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Working, stable model (Nov 2025)
MODEL = "llama-3.1-8b-instant"


def answer_question(query, chunks, chat_history):
    """
    Main Q&A function using Groq model.
    Matches query with document chunks, builds context, and returns answer + context.
    """
    # Build document context
    context = ""
    for c in chunks:
        if any(word.lower() in c.lower() for word in query.split()):
            context += c + "\n---\n"

    if context.strip() == "":
        context = "No direct match found in the document."

    # Chat prompt
    messages = [
        {"role": "system", "content": "You are SmartDocs AI. Answer ONLY using the provided document context."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{query}"}
    ]

    # Groq API call
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.2
    )

    # FIX: Groq returns message.content – NOT dict
    answer = response.choices[0].message.content
    return answer, context



def generate_summary(full_text):
    """
    Generates document summary using Groq.
    """
    messages = [
        {"role": "user", "content": f"Summarize the following document clearly:\n\n{full_text}"}
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.3
    )

    return response.choices[0].message.content



def extract_keywords(full_text):
    """
    Extracts important keywords/topics from the document.
    """
    messages = [
        {"role": "user", "content": f"Extract 5–10 key keywords or topics from the document:\n\n{full_text}"}
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.3
    )

    return response.choices[0].message.content
