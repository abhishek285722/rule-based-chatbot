"""
app.py - Streamlit Chat UI for Rule-Based Chatbot
Task 5: Rule-Based Chatbot Implementation

Features:
- Modern conversational UI with st.chat_message and st.chat_input
- Automatic welcome greeting on first session load
- Clickable suggestion chips for instant query testing
- Intent transparency tags and conversation analytics
- Interactive sidebar with Intent Knowledge Explorer
- One-click Clear Chat and Clean 'Stop Session' shutdown
"""

import os
import time
import datetime
import streamlit as st
import chatbot

# -------------------------------------------------------------
# 1. Page Configuration & Custom Styling
# -------------------------------------------------------------
st.set_page_config(
    page_title="Rule-Based Chatbot | PyBot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    /* Global Page Styling */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        color: #f8fafc;
    }
    
    /* Header Banner */
    .header-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(12px);
    }
    
    .header-title {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #818cf8 0%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .header-sub {
        color: #94a3b8;
        font-size: 0.95rem;
        margin-top: 6px;
        margin-bottom: 0;
    }
    
    /* Intent badge */
    .intent-badge {
        display: inline-block;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 3px 8px;
        border-radius: 6px;
        background: rgba(99, 102, 241, 0.2);
        color: #a5b4fc;
        border: 1px solid rgba(99, 102, 241, 0.4);
        margin-bottom: 6px;
    }
    
    .time-stamp {
        font-size: 0.72rem;
        color: #64748b;
        margin-left: 8px;
    }
    
    /* Suggestions Container */
    .suggestions-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #94a3b8;
        margin-bottom: 8px;
    }
    
    /* Streamlit Chat tweaks */
    div[data-testid="stChatMessage"] {
        background-color: rgba(30, 41, 59, 0.55);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #0b0f19;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------
# 2. Session State Initialization
# -------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Enhancement 3: Welcome Message on First Load
if not st.session_state.messages:
    welcome_time = datetime.datetime.now().strftime("%I:%M %p")
    st.session_state.messages.append({
        "role": "assistant",
        "content": (
            "👋 **Hello! I'm PyBot, your Rule-Based Conversational Assistant.**\n\n"
            "I operate strictly using deterministic Python dictionary patterns and keyword rules without machine learning!\n\n"
            "Here are things you can ask me:\n"
            "- Greet me or ask who I am\n"
            "- Ask for a joke or inspirational quote\n"
            "- Ask for the current time or today's date\n"
            "- Solve simple math (e.g., `what is 45 * 6`)\n"
            "- Type **'help'** anytime to see everything I understand!\n\n"
            "Click any suggestion chip below or type in the input bar to chat!"
        ),
        "intent": "welcome",
        "timestamp": welcome_time,
    })

# Pending prompt handler for quick chips
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


def handle_user_input(user_text: str):
    """Processes user text and adds response to chat history."""
    if not user_text or not user_text.strip():
        return
    
    curr_time = datetime.datetime.now().strftime("%I:%M %p")
    
    # 1. Append user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_text.strip(),
        "intent": None,
        "timestamp": curr_time,
    })
    
    # 2. Get bot response & intent
    bot_reply, intent_name = chatbot.get_response_with_intent(user_text)
    
    # 3. Append bot message
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply,
        "intent": intent_name,
        "timestamp": curr_time,
    })


# -------------------------------------------------------------
# 3. Sidebar: Metadata, Intent Explorer, Stats & Stop Session
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🤖 PyBot Control Panel")
    st.caption("Task 5 — Rule-Based Virtual Assistant")
    
    st.markdown(
        """
        - **Architecture**: Dictionary & Regex Rule Matching
        - **Engine**: Pure Python (`re`, `datetime`, `random`)
        - **Framework**: Streamlit Chat Component
        """
    )
    st.divider()
    
    # Conversation Statistics
    user_msgs = [m for m in st.session_state.messages if m["role"] == "user"]
    bot_msgs = [m for m in st.session_state.messages if m["role"] == "assistant"]
    matched_msgs = [m for m in bot_msgs if m.get("intent") not in ["unknown", "welcome", "empty"]]
    unknown_msgs = [m for m in bot_msgs if m.get("intent") == "unknown"]
    
    st.subheader("📊 Session Statistics")
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric("Total Messages", len(st.session_state.messages))
        st.metric("Matched Rules", len(matched_msgs))
    with col_stat2:
        st.metric("User Queries", len(user_msgs))
        st.metric("Fallbacks", len(unknown_msgs))
        
    st.divider()
    
    # Intent Knowledge Base Explorer
    st.subheader("📖 Supported Intents")
    with st.expander("🔍 View All 12+ Intents & Triggers", expanded=False):
        intents_dict = chatbot.get_supported_intents()
        for key, info in intents_dict.items():
            st.markdown(f"**{info['title']}** (`{key}`)")
            triggers = ", ".join([f"`{p}`" for p in info["samples"]])
            st.caption(f"Triggers: {triggers}")
            st.markdown("---")
            
    st.divider()
    
    # Actions: Clear Chat & Stop Session
    st.subheader("⚡ Session Controls")
    
    if st.button("🗑️ Clear Conversation", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.rerun()
        
    if st.button("🛑 Stop Session", use_container_width=True, type="primary", help="Stop server and close dedicated window"):
        st.info("Stopping application and closing window...")
        time.sleep(0.5)
        os._exit(0)


# -------------------------------------------------------------
# 4. Main Chat Interface
# -------------------------------------------------------------
# Header Card
st.markdown(
    """
    <div class="header-card">
        <h1 class="header-title">🤖 Rule-Based Chatbot</h1>
        <p class="header-sub">
            Task 5: Pure Python Keyword & Pattern Matching Virtual Assistant • Instant & Deterministic Responses
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Enhancement 1: Suggestion Quick Chips
st.markdown('<div class="suggestions-label">💡 Try asking or click a suggestion:</div>', unsafe_allow_html=True)
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    if st.button("👋 Hello!", use_container_width=True):
        st.session_state.pending_prompt = "Hello!"
with col2:
    if st.button("😂 Tell a joke", use_container_width=True):
        st.session_state.pending_prompt = "Tell me a joke"
with col3:
    if st.button("⏰ Current time", use_container_width=True):
        st.session_state.pending_prompt = "What time is it?"
with col4:
    if st.button("📅 Today's date", use_container_width=True):
        st.session_state.pending_prompt = "What is today's date?"
with col5:
    if st.button("✨ Daily quote", use_container_width=True):
        st.session_state.pending_prompt = "Inspire me"
with col6:
    if st.button("🔢 Solve math", use_container_width=True):
        st.session_state.pending_prompt = "What is 45 * 12?"

# Check if a chip button was clicked
if st.session_state.pending_prompt:
    prompt_to_run = st.session_state.pending_prompt
    st.session_state.pending_prompt = None
    handle_user_input(prompt_to_run)
    st.rerun()

st.divider()

# Render Chat Messages
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="🧑‍💻" if msg["role"] == "user" else "🤖"):
            if msg["role"] == "assistant" and msg.get("intent"):
                intent_display = msg['intent'].replace('_', ' ')
                st.markdown(
                    f"<span class='intent-badge'>{intent_display}</span>"
                    f"<span class='time-stamp'>{msg.get('timestamp', '')}</span>",
                    unsafe_allow_html=True,
                )
            st.markdown(msg["content"])

# User Chat Input
user_query = st.chat_input("Type your message here (e.g. 'what time is it', 'tell me a joke', 'who created you')...")
if user_query:
    handle_user_input(user_query)
    st.rerun()
