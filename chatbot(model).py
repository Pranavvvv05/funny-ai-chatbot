from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

st.set_page_config(
   page_title="Funny AI Chat",
   page_icon="🤖",
   layout="centered"
)

st.markdown("""
<style>
   @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

   html, body, [data-testid="stAppViewContainer"] {
       background: #0a0a0f !important;
       color: #e8e8f0;
       font-family: 'Inter', sans-serif;
   }
   [data-testid="stHeader"] { background: transparent !important; }
   [data-testid="stMain"] { background: transparent !important; }
   .block-container { background: transparent !important; }

   #particle-canvas {
       position: fixed;
       top: 0; left: 0;
       width: 100vw;
       height: 100vh;
       z-index: 0;
       pointer-events: none;
   }

   .topbar {
       display: flex;
       align-items: center;
       gap: 14px;
       padding: 1.2rem 0 0.8rem;
       border-bottom: 1px solid rgba(255,255,255,0.07);
       margin-bottom: 1rem;
       position: relative;
       z-index: 10;
   }
   .bot-avatar {
       width: 46px; height: 46px;
       border-radius: 50%;
       background: linear-gradient(135deg, #667eea, #764ba2);
       display: flex;
       align-items: center;
       justify-content: center;
       font-size: 1.3rem;
       flex-shrink: 0;
       box-shadow: 0 0 16px rgba(102,126,234,0.4);
   }
   .bot-name {
       font-size: 1rem;
       font-weight: 600;
       color: #ffffff;
   }
   .bot-status {
       font-size: 0.72rem;
       color: #22c55e;
       display: flex;
       align-items: center;
       gap: 4px;
   }
   .dot { width:6px; height:6px; border-radius:50%; background:#22c55e; display:inline-block; }

   .msg-row {
       display: flex;
       align-items: flex-end;
       gap: 8px;
       margin: 0.45rem 0;
       position: relative;
       z-index: 10;
   }
   .msg-row.user  { justify-content: flex-end; }
   .msg-row.bot   { justify-content: flex-start; }

   .mini-avatar {
       width: 28px; height: 28px;
       border-radius: 50%;
       background: linear-gradient(135deg, #667eea, #764ba2);
       display: flex; align-items: center; justify-content: center;
       font-size: 0.75rem; flex-shrink: 0;
       box-shadow: 0 0 8px rgba(102,126,234,0.3);
   }
   .mini-avatar-user {
       width: 28px; height: 28px;
       border-radius: 50%;
       background: linear-gradient(135deg, #f093fb, #f5576c);
       display: flex; align-items: center; justify-content: center;
       font-size: 0.75rem; flex-shrink: 0;
   }

   .bubble {
       max-width: 68%;
       padding: 0.65rem 1rem;
       font-size: 0.88rem;
       line-height: 1.55;
       word-wrap: break-word;
   }
   .bubble.user {
       background: linear-gradient(135deg, #667eea, #764ba2);
       color: #fff;
       border-radius: 18px 18px 4px 18px;
       box-shadow: 0 2px 12px rgba(102,126,234,0.25);
   }
   .bubble.bot {
       background: rgba(255,255,255,0.05);
       color: #e8e8f0;
       border-radius: 18px 18px 18px 4px;
       border: 1px solid rgba(255,255,255,0.08);
       backdrop-filter: blur(10px);
   }

   [data-testid="stChatInput"] textarea {
       background: rgba(255,255,255,0.05) !important;
       color: #e8e8f0 !important;
       border: 1px solid rgba(255,255,255,0.1) !important;
       border-radius: 12px !important;
       font-family: 'Inter', sans-serif !important;
   }
   [data-testid="stChatInput"] textarea:focus {
       border-color: #667eea !important;
       box-shadow: 0 0 0 3px rgba(102,126,234,0.2) !important;
   }

   #MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }
</style>

<canvas id="particle-canvas"></canvas>

<script>
const canvas = document.getElementById('particle-canvas');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

window.addEventListener('resize', () => {
   canvas.width = window.innerWidth;
   canvas.height = window.innerHeight;
});

const particles = [];
const count = 90;

for (let i = 0; i < count; i++) {
   particles.push({
       x: Math.random() * canvas.width,
       y: Math.random() * canvas.height,
       r: Math.random() * 1.8 + 0.4,
       dx: (Math.random() - 0.5) * 0.4,
       dy: (Math.random() - 0.5) * 0.4,
       alpha: Math.random() * 0.5 + 0.1
   });
}

function draw() {
   ctx.clearRect(0, 0, canvas.width, canvas.height);

   for (let i = 0; i < particles.length; i++) {
       for (let j = i + 1; j < particles.length; j++) {
           const dx = particles[i].x - particles[j].x;
           const dy = particles[i].y - particles[j].y;
           const dist = Math.sqrt(dx*dx + dy*dy);
           if (dist < 120) {
               ctx.beginPath();
               ctx.strokeStyle = `rgba(102,126,234,${0.12 * (1 - dist/120)})`;
               ctx.lineWidth = 0.5;
               ctx.moveTo(particles[i].x, particles[i].y);
               ctx.lineTo(particles[j].x, particles[j].y);
               ctx.stroke();
           }
       }
   }

   particles.forEach(p => {
       ctx.beginPath();
       ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
       ctx.fillStyle = `rgba(150,170,255,${p.alpha})`;
       ctx.fill();

       p.x += p.dx;
       p.y += p.dy;

       if (p.x < 0 || p.x > canvas.width)  p.dx *= -1;
       if (p.y < 0 || p.y > canvas.height) p.dy *= -1;
   });

   requestAnimationFrame(draw);
}

draw();
</script>
""", unsafe_allow_html=True)

# ── Model init ────────────────────────────────────────────────────────────────
@st.cache_resource
def get_model():
   import os
   os.environ["MISTRAL_API_KEY"] = st.secrets["MISTRAL_API_KEY"]
   return ChatMistralAI(model="mistral-small-2506", temperature=0.9)

model = get_model()

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
   st.session_state.messages = [
       SystemMessage(content="you are a funny AI agent")
   ]

# ── Top bar ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
   <div class="bot-avatar">🤖</div>
   <div>
       <div class="bot-name">Funny AI</div>
       <div class="bot-status"><span class="dot"></span> Online · Powered by Mistral</div>
   </div>
</div>
""", unsafe_allow_html=True)

# ── Render conversation ───────────────────────────────────────────────────────
for msg in st.session_state.messages:
   if isinstance(msg, HumanMessage):
       st.markdown(
           f'''<div class="msg-row user">
                 <div class="bubble user">{msg.content}</div>
                 <div class="mini-avatar-user">👤</div>
               </div>''',
           unsafe_allow_html=True
       )
   elif isinstance(msg, AIMessage):
       st.markdown(
           f'''<div class="msg-row bot">
                 <div class="mini-avatar">🤖</div>
                 <div class="bubble bot">{msg.content}</div>
               </div>''',
           unsafe_allow_html=True
       )

# ── Chat input ────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Type a message..."):
   st.session_state.messages.append(HumanMessage(content=prompt))
   st.markdown(
       f'''<div class="msg-row user">
             <div class="bubble user">{prompt}</div>
             <div class="mini-avatar-user">👤</div>
           </div>''',
       unsafe_allow_html=True
   )

   with st.spinner(""):
       response = model.invoke(st.session_state.messages)

   st.session_state.messages.append(AIMessage(content=response.content))
   st.markdown(
       f'''<div class="msg-row bot">
             <div class="mini-avatar">🤖</div>
             <div class="bubble bot">{response.content}</div>
           </div>''',
       unsafe_allow_html=True
   )

   st.rerun()