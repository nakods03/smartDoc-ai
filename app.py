import streamlit as st
from dotenv import load_dotenv
from document_loader import extract_text_from_pdf, chunk_text
from chat_engine import answer_question, generate_summary, extract_keywords
import time

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="SmartDocs AI",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
    <style>
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1e1e 0%, #2d2d2d 100%);
    }
    
    [data-testid="stSidebar"] .stButton>button {
        width: 100%;
        background-color: #2d2d2d;
        color: white;
        border: 1px solid #404040;
        border-radius: 8px;
        padding: 0.75rem;
        margin: 0.5rem 0;
        transition: all 0.3s;
    }
    
    [data-testid="stSidebar"] .stButton>button:hover {
        background-color: #3d3d3d;
        border-color: #555;
        transform: translateX(5px);
    }
    
    /* Chat bubble styling */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        padding: 1rem 0;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 18px 18px 4px 18px;
        margin-left: auto;
        max-width: 70%;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        word-wrap: break-word;
    }
    
    .assistant-message {
        background: #2d2d2d;
        color: #e0e0e0;
        padding: 1rem 1.5rem;
        border-radius: 18px 18px 18px 4px;
        margin-right: auto;
        max-width: 70%;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        border: 1px solid #404040;
        word-wrap: break-word;
    }
    
    /* Summary and insights styling */
    .info-card {
        background: #2d2d2d;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #404040;
        margin: 1rem 0;
    }
    
    .metric-box {
        background: #1e1e1e;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    
    /* Search result styling */
    .search-result {
        background: #2d2d2d;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #404040;
        margin: 0.5rem 0;
        border-left: 4px solid #4CAF50;
    }
    
    .highlight {
        background-color: #ffd700;
        color: #000;
        padding: 2px 4px;
        border-radius: 3px;
        font-weight: bold;
    }
    
    /* Typography */
    h1 {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        margin-top: 2rem !important;
    }
    
    h3 {
        font-size: 1.3rem !important;
        font-weight: 600 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "chunks" not in st.session_state:
    st.session_state.chunks = None

if "chat" not in st.session_state:
    st.session_state.chat = []

if "full_text" not in st.session_state:
    st.session_state.full_text = None

if "document_metadata" not in st.session_state:
    st.session_state.document_metadata = None

if "current_mode" not in st.session_state:
    st.session_state.current_mode = "upload"

if "summary" not in st.session_state:
    st.session_state.summary = None

if "keywords" not in st.session_state:
    st.session_state.keywords = None

# Sidebar
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style="font-size: 2rem; margin: 0; color: #667eea;">📘 SmartDocs AI</h1>
            <p style="color: #888; margin-top: 0.5rem;">Knowledge Base Agent</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation buttons
    if st.button("📤 Upload Document", use_container_width=True):
        st.session_state.current_mode = "upload"
        st.rerun()
    
    if st.button("💬 Chat", use_container_width=True):
        st.session_state.current_mode = "chat"
        st.rerun()
    
    if st.button("📄 Summary", use_container_width=True):
        st.session_state.current_mode = "summary"
        st.rerun()
    
    if st.button("🔍 Search", use_container_width=True):
        st.session_state.current_mode = "search"
        st.rerun()
    
    if st.button("📊 Insights", use_container_width=True):
        st.session_state.current_mode = "insights"
        st.rerun()
    
    st.markdown("---")
    
    # Document status
    if st.session_state.document_metadata:
        st.markdown("### 📋 Document Status")
        st.success("✅ Document Loaded")
        st.caption(f"Pages: {st.session_state.document_metadata['page_count']}")
        st.caption(f"Words: {st.session_state.document_metadata['word_count']:,}")
    else:
        st.info("📤 Upload a PDF to get started")

# Main content area
if st.session_state.current_mode == "upload":
    st.title("📤 Upload Document")
    st.markdown("### Upload a PDF document to begin analyzing")
    
    uploaded = st.file_uploader("Choose a PDF file", type=["pdf"], label_visibility="collapsed")
    
    if uploaded:
        with st.spinner("🔄 Processing PDF... This may take a moment."):
            result = extract_text_from_pdf(uploaded)
            st.session_state.full_text = result["text"]
            st.session_state.chunks = chunk_text(result["text"])
            st.session_state.document_metadata = {
                "page_count": result["page_count"],
                "word_count": result["word_count"],
                "chunk_count": len(st.session_state.chunks)
            }
            # Reset summary and keywords when new document is uploaded
            st.session_state.summary = None
            st.session_state.keywords = None
        
        st.success("✅ PDF processed successfully!")
        st.balloons()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Pages", st.session_state.document_metadata["page_count"])
        with col2:
            st.metric("Words", f"{st.session_state.document_metadata['word_count']:,}")
        with col3:
            st.metric("Chunks", st.session_state.document_metadata["chunk_count"])
        
        st.info("💡 Navigate to Chat, Summary, Search, or Insights using the sidebar to explore your document.")

elif st.session_state.current_mode == "chat":
    st.title("💬 Chat with Your Document")
    
    if st.session_state.chunks is None:
        st.warning("⚠️ Please upload a PDF document first using the sidebar.")
    else:
        # Chat interface
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Display chat history
        for msg in st.session_state.chat:
            if msg["role"] == "user":
                st.markdown(f'<div class="user-message">🧑 <strong>You</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-message">🤖 <strong>SmartDocs AI</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat input
        st.markdown("---")
        query = st.text_input("Ask a question about the document", key="chat_input", label_visibility="collapsed")
        
        col1, col2 = st.columns([1, 10])
        with col1:
            ask_button = st.button("Send", type="primary", use_container_width=True)
        
        if ask_button and query:
            with st.spinner("🤔 Thinking..."):
                answer, context = answer_question(query, st.session_state.chunks, st.session_state.chat)
                st.session_state.chat.append({"role": "user", "content": query})
                st.session_state.chat.append({"role": "assistant", "content": answer})
                st.rerun()

elif st.session_state.current_mode == "summary":
    st.title("📄 Document Summary")
    
    if st.session_state.full_text is None:
        st.warning("⚠️ Please upload a PDF document first using the sidebar.")
    else:
        if st.session_state.summary is None:
            with st.spinner("🔄 Generating comprehensive summary... This may take a moment."):
                st.session_state.summary = generate_summary(st.session_state.full_text)
        
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 📋 Summary")
        st.markdown(st.session_state.summary)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🔄 Regenerate Summary"):
            st.session_state.summary = None
            st.rerun()

elif st.session_state.current_mode == "search":
    st.title("🔍 Search Document")
    
    if st.session_state.chunks is None:
        st.warning("⚠️ Please upload a PDF document first using the sidebar.")
    else:
        search_query = st.text_input("Enter search term", placeholder="Search for keywords, phrases, or topics...")
        
        if search_query:
            # Search through chunks
            matching_chunks = []
            for i, chunk in enumerate(st.session_state.chunks):
                if search_query.lower() in chunk.lower():
                    matching_chunks.append((i, chunk))
            
            if matching_chunks:
                st.success(f"✅ Found {len(matching_chunks)} matching chunk(s)")
                
                for idx, (chunk_num, chunk) in enumerate(matching_chunks):
                    # Highlight the search term
                    highlighted_chunk = chunk.replace(
                        search_query,
                        f'<span class="highlight">{search_query}</span>'
                    )
                    highlighted_chunk = highlighted_chunk.replace(
                        search_query.lower(),
                        f'<span class="highlight">{search_query}</span>'
                    )
                    highlighted_chunk = highlighted_chunk.replace(
                        search_query.capitalize(),
                        f'<span class="highlight">{search_query}</span>'
                    )
                    
                    st.markdown(f'<div class="search-result">', unsafe_allow_html=True)
                    st.markdown(f"**Chunk {chunk_num + 1}**")
                    st.markdown(highlighted_chunk, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("🔍 No matching chunks found. Try different keywords.")

elif st.session_state.current_mode == "insights":
    st.title("📊 Document Insights")
    
    if st.session_state.document_metadata is None:
        st.warning("⚠️ Please upload a PDF document first using the sidebar.")
    else:
        # Calculate reading time (average 200 words per minute)
        reading_time = max(1, round(st.session_state.document_metadata["word_count"] / 200))
        
        # Generate keywords if not already generated
        if st.session_state.keywords is None and st.session_state.full_text:
            with st.spinner("🔄 Extracting keywords..."):
                st.session_state.keywords = extract_keywords(st.session_state.full_text)
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-box">', unsafe_allow_html=True)
            st.metric("📄 Total Pages", st.session_state.document_metadata["page_count"])
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-box">', unsafe_allow_html=True)
            st.metric("📝 Word Count", f"{st.session_state.document_metadata['word_count']:,}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-box">', unsafe_allow_html=True)
            st.metric("📦 Number of Chunks", st.session_state.document_metadata["chunk_count"])
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-box">', unsafe_allow_html=True)
            st.metric("⏱️ Reading Time", f"~{reading_time} min")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Keywords section
        if st.session_state.keywords:
            st.markdown("---")
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.markdown("### 🔑 Key Topics & Keywords")
            st.markdown(st.session_state.keywords)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Additional statistics
        st.markdown("---")
        st.markdown("### 📈 Additional Statistics")
        
        col1, col2 = st.columns(2)
        with col1:
            avg_words_per_page = st.session_state.document_metadata["word_count"] / st.session_state.document_metadata["page_count"]
            st.info(f"**Average words per page:** {avg_words_per_page:.0f}")
        
        with col2:
            avg_words_per_chunk = st.session_state.document_metadata["word_count"] / st.session_state.document_metadata["chunk_count"]
            st.info(f"**Average words per chunk:** {avg_words_per_chunk:.0f}")
