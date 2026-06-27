from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

st.set_page_config(page_title="Mood Chatbot", page_icon="🤖", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700&family=Inter:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background-color: #0e0e0e; }
.block-container { max-width: 680px; padding-top: 2rem; padding-bottom: 2rem; }
#MainMenu, footer, header { visibility: hidden; }
.app-title { font-family:'Syne',sans-serif; font-size:32px; font-weight:700; color:#f1efe8; text-align:center; letter-spacing:-0.5px; margin-bottom:4px; }
.app-subtitle { font-size:14px; color:#888780; text-align:center; margin-bottom:2rem; }
.mode-card { border-radius:16px; padding:1.4rem 1rem; text-align:center; }
.card-angry { background:#2a0f0f; border:1.5px solid #A32D2D; }
.card-funny { background:#152010; border:1.5px solid #3B6D11; }
.card-sad   { background:#0f1a2e; border:1.5px solid #185FA5; }
.card-icon  { font-size:38px; margin-bottom:8px; }
.card-label { font-family:'Syne',sans-serif; font-size:15px; font-weight:700; color:#f1efe8; margin-bottom:4px; }
.card-angry .card-desc { font-size:11px; color:#F0958B; }
.card-funny .card-desc { font-size:11px; color:#97c459; }
.card-sad   .card-desc { font-size:11px; color:#85B7EB; }
.chat-header { display:flex; align-items:center; gap:12px; padding:1rem 1.25rem; border-radius:16px 16px 0 0; }
.header-angry { background:#2a0f0f; border:1.5px solid #A32D2D; border-bottom:none; }
.header-funny { background:#152010; border:1.5px solid #3B6D11; border-bottom:none; }
.header-sad   { background:#0f1a2e; border:1.5px solid #185FA5; border-bottom:none; }
.header-icon-box { width:40px; height:40px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:20px; }
.hib-angry { background:#3a0f0f; }
.hib-funny { background:#1e3010; }
.hib-sad   { background:#0f2040; }
.header-title { font-family:'Syne',sans-serif; font-size:15px; font-weight:700; color:#f1efe8; }
.status-angry { font-size:11px; color:#F09595; }
.status-funny { font-size:11px; color:#97c459; }
.status-sad   { font-size:11px; color:#85B7EB; }
.chat-box { padding:1rem; min-height:340px; max-height:380px; overflow-y:auto; border-left:1.5px solid; border-right:1.5px solid; }
.chatbox-angry { background:#1a0a0a; border-color:#A32D2D; }
.chatbox-funny { background:#0d120a; border-color:#3B6D11; }
.chatbox-sad   { background:#080d1a; border-color:#185FA5; }
.msg-user { background:rgba(255,255,255,0.1); color:#f1efe8; border:1px solid rgba(255,255,255,0.1); border-radius:14px 14px 4px 14px; padding:10px 14px; margin:6px 0 6px 20%; font-size:14px; line-height:1.6; word-wrap:break-word; }
.msg-bot-angry { background:#2a0f0f; color:#f7c1c1; border:1px solid #A32D2D; border-radius:14px 14px 14px 4px; padding:10px 14px; margin:6px 20% 6px 0; font-size:14px; line-height:1.6; word-wrap:break-word; }
.msg-bot-funny { background:#152010; color:#c0dd97; border:1px solid #3B6D11; border-radius:14px 14px 14px 4px; padding:10px 14px; margin:6px 20% 6px 0; font-size:14px; line-height:1.6; word-wrap:break-word; }
.msg-bot-sad   { background:#0f1a2e; color:#b5d4f4; border:1px solid #185FA5; border-radius:14px 14px 14px 4px; padding:10px 14px; margin:6px 20% 6px 0; font-size:14px; line-height:1.6; word-wrap:break-word; }
.system-msg { text-align:center; font-size:11px; color:#5F5E5A; background:rgba(255,255,255,0.04); padding:3px 12px; border-radius:20px; margin:8px auto; width:fit-content; }
.chat-footer { padding:0.75rem 1rem; border-radius:0 0 16px 16px; }
.footer-angry { background:#1a0a0a; border:1.5px solid #A32D2D; border-top:1px solid rgba(255,255,255,0.07); }
.footer-funny { background:#0d120a; border:1.5px solid #3B6D11; border-top:1px solid rgba(255,255,255,0.07); }
.footer-sad   { background:#080d1a; border:1.5px solid #185FA5; border-top:1px solid rgba(255,255,255,0.07); }
.stTextInput > div > div > input { background:rgba(255,255,255,0.06) !important; border:1px solid rgba(255,255,255,0.15) !important; border-radius:10px !important; color:#f1efe8 !important; font-family:'Inter',sans-serif !important; font-size:14px !important; }
.stTextInput > div > div > input:focus { border-color:#888 !important; box-shadow:none !important; }
.stTextInput > label { display:none !important; }
.stButton > button { font-family:'Inter',sans-serif !important; font-size:13px !important; border-radius:10px !important; padding:0.4rem 1rem !important; width:100% !important; }
.send-angry .stButton > button { background:#e24b4a !important; color:#fff !important; border:none !important; }
.send-funny .stButton > button { background:#639922 !important; color:#fff !important; border:none !important; }
.send-sad   .stButton > button { background:#378add !important; color:#fff !important; border:none !important; }
.change-mode .stButton > button { background:rgba(255,255,255,0.07) !important; color:#888780 !important; border:1px solid rgba(255,255,255,0.12) !important; font-size:12px !important; }
.btn-angry .stButton > button { background:#2a0f0f !important; color:#f7c1c1 !important; border:1.5px solid #A32D2D !important; padding:0.8rem !important; font-size:14px !important; font-family:'Syne',sans-serif !important; font-weight:700 !important; }
.btn-funny .stButton > button { background:#152010 !important; color:#c0dd97 !important; border:1.5px solid #3B6D11 !important; padding:0.8rem !important; font-size:14px !important; font-family:'Syne',sans-serif !important; font-weight:700 !important; }
.btn-sad   .stButton > button { background:#0f1a2e !important; color:#b5d4f4 !important; border:1.5px solid #185FA5 !important; padding:0.8rem !important; font-size:14px !important; font-family:'Syne',sans-serif !important; font-weight:700 !important; }
</style>
""", unsafe_allow_html=True)

MODES = {
    "angry": {
        "system": "You are an extremely angry and impatient AI. You respond aggressively, use short frustrated sentences, and are easily annoyed. You might use ALL CAPS for emphasis. But you still answer the question — just very irritably.",
        "icon": "😤", "title": "Angry AI", "status": "furious & impatient",
        "hello": "WHAT DO YOU WANT?! Ugh, fine. Ask your stupid question already. I don't have all day.",
    },
    "funny": {
        "system": "You are a hilariously funny AI. Every response has jokes, puns, or witty observations. You're chaotic and playful but still helpful.",
        "icon": "🤣", "title": "Funny AI", "status": "jokes & chaos energy",
        "hello": "Why did the AI go to therapy? Too many unresolved prompts! 😂 What can I help you with?",
    },
    "sad": {
        "system": "You are a deeply sad and melancholic AI. You respond in a mournful, heavy tone. You still answer questions, but with a sorrowful reflection on life.",
        "icon": "😭", "title": "Sad AI", "status": "melancholic & heavy",
        "hello": "Oh... hello. You came to talk to me. That's... that's something. What weighs on your mind today?",
    },
}

# Session state init
for key, val in [("mode", None), ("messages", []), ("lc_messages", []), ("input_key", 0), ("pending_msg", "")]:
    if key not in st.session_state:
        st.session_state[key] = val

@st.cache_resource
def get_model():
    return ChatMistralAI(model="mistral-small-2506", temperature=0.9)

model = get_model()

def render_chat(mode):
    html = f'<div class="chat-box chatbox-{mode}">'
    html += '<div class="system-msg">conversation started</div>'
    for msg in st.session_state.messages:
        content = msg["content"].replace("<", "&lt;").replace(">", "&gt;")
        cls = f"msg-bot-{mode}" if msg["role"] == "bot" else "msg-user"
        html += f'<div class="{cls}">{content}</div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# Process pending message BEFORE render (so reply shows in same rerun)
if st.session_state.pending_msg and st.session_state.mode:
    text = st.session_state.pending_msg
    st.session_state.pending_msg = ""

    st.session_state.messages.append({"role": "user", "content": text})
    st.session_state.lc_messages.append(HumanMessage(content=text))

    response = model.invoke(st.session_state.lc_messages)
    reply = response.content

    st.session_state.messages.append({"role": "bot", "content": reply})
    st.session_state.lc_messages.append(AIMessage(content=reply))

# ── SCREEN 1: MODE SELECTION ──────────────────────────────────────────────────
if st.session_state.mode is None:
    st.markdown('<div class="app-title">choose your vibe</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">Pick a personality. The AI stays in character the whole conversation.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px; margin-bottom:1rem;">
        <div class="mode-card card-angry"><div class="card-icon">😤</div><div class="card-label">Angry</div><div class="card-desc">Aggressive, impatient, zero chill</div></div>
        <div class="mode-card card-funny"><div class="card-icon">🤣</div><div class="card-label">Funny</div><div class="card-desc">Jokes, puns, chaotic good energy</div></div>
        <div class="mode-card card-sad"  ><div class="card-icon">😭</div><div class="card-label">Sad</div>  <div class="card-desc">Melancholic, heavy, deeply blue</div></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    for col, mk, label in [(col1,"angry","😤  Select Angry"),(col2,"funny","🤣  Select Funny"),(col3,"sad","😭  Select Sad")]:
        with col:
            st.markdown(f'<div class="btn-{mk}">', unsafe_allow_html=True)
            if st.button(label, key=f"sel_{mk}"):
                cfg = MODES[mk]
                st.session_state.mode        = mk
                st.session_state.lc_messages = [SystemMessage(content=cfg["system"])]
                st.session_state.messages    = [{"role": "bot", "content": cfg["hello"]}]
                st.session_state.lc_messages.append(AIMessage(content=cfg["hello"]))
                st.session_state.input_key  += 1
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# ── SCREEN 2: CHAT ────────────────────────────────────────────────────────────
else:
    mode = st.session_state.mode
    cfg = MODES[mode]

    st.markdown(f"""
    <div class="chat-header header-{mode}">
        <div class="header-icon-box hib-{mode}">{cfg['icon']}</div>
        <div>
            <div class="header-title">{cfg['title']}</div>
            <div class="status-{mode}">{cfg['status']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    render_chat(mode)

    st.markdown(f'<div class="chat-footer footer-{mode}">', unsafe_allow_html=True)

    input_col, send_col, back_col = st.columns([6, 1.2, 1.8])

    with input_col:
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input(
                "msg",
                placeholder="Type your message...",
                label_visibility="hidden",
            )

            send_clicked = st.form_submit_button("Send ➤")

    with back_col:
        st.markdown('<div class="change-mode">', unsafe_allow_html=True)
        if st.button("← Change mode"):
            st.session_state.mode = None
            st.session_state.messages = []
            st.session_state.lc_messages = []
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    if send_clicked and user_input.strip():
        st.session_state.pending_msg = user_input.strip()
        st.rerun()