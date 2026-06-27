from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Funny AI Chat",
    page_icon="🤖",
    layout="centered"
)

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── base ── */
    html, body, [data-testid="stAppViewContainer"] {
        background: #0d0d0d;
        color: #f0f0f0;
        font-family: 'Inter', sans-serif;
    }
    [data-testid="stHeader"] { background: transparent; }

    /* ── title ── */
    .chat-title {
        text-align: center;
        padding: 1.5rem 0 0.25rem;
        font-size: 1.8rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        color: #ffffff;
    }
    .chat-subtitle {
        text-align: center;
        font-size: 0.85rem;
        color: #888;
        margin-bottom: 1.5rem;
    }

    /* ── chat bubbles ── */
    .msg-row {
        display: flex;
        margin: 0.4rem 0;
    }
    .msg-row.user  { justify-content: flex-end; }
    .msg-row.bot   { justify-content: flex-start; }

    .bubble {
        max-width: 72%;
        padding: 0.65rem 1rem;
        border-radius: 18px;
        font-size: 0.92rem;
        line-height: 1.5;
        word-wrap: break-word;
    }
    .bubble.user {
        background: #6c3bff;
        color: #fff;
        border-bottom-right-radius: 4px;
    }
    .bubble.bot {
        background: #1e1e1e;
        color: #f0f0f0;
        border: 1px solid #2a2a2a;
        border-bottom-left-radius: 4px;
    }

    /* ── input area ── */
    [data-testid="stChatInput"] textarea {
        background: #1a1a1a !important;
        color: #f0f0f0 !important;
        border: 1px solid #333 !important;
        border-radius: 12px !important;
    }
    [data-testid="stChatInput"] textarea:focus {
        border-color: #6c3bff !important;
        box-shadow: 0 0 0 2px rgba(108,59,255,0.25) !important;
    }

    /* ── hide streamlit chrome ── */
    #MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Model init (cached so it doesn't reload on every rerun) ───────────────────
@st.cache_resource
def get_model():
    return ChatMistralAI(model="mistral-small-2506", temperature=0.9)

model = get_model()

# ── Session state: message history ───────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="you are a funny AI agent")
    ]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="chat-title">🤖 Funny AI</div>', unsafe_allow_html=True)
st.markdown('<div class="chat-subtitle">Powered by Mistral · Always in a mood to roast 😄</div>', unsafe_allow_html=True)

# ── Render existing conversation ─────────────────────────────────────────────
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        st.markdown(
            f'<div class="msg-row user"><div class="bubble user">{msg.content}</div></div>',
            unsafe_allow_html=True
        )
    elif isinstance(msg, AIMessage):
        st.markdown(
            f'<div class="msg-row bot"><div class="bubble bot">{msg.content}</div></div>',
            unsafe_allow_html=True
        )

# ── Chat input ────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Say something..."):
    # Append user message
    st.session_state.messages.append(HumanMessage(content=prompt))
    st.markdown(
        f'<div class="msg-row user"><div class="bubble user">{prompt}</div></div>',
        unsafe_allow_html=True
    )

    # Get response
    with st.spinner("thinking..."):
        response = model.invoke(prompt)

    # Append & show bot message
    st.session_state.messages.append(AIMessage(content=response.content))
    st.markdown(
        f'<div class="msg-row bot"><div class="bubble bot">{response.content}</div></div>',
        unsafe_allow_html=True
    )

