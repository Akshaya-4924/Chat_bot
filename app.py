"""
app.py - Chat-style UI for Agentic AI
Run with: streamlit run app.py
"""

import streamlit as st

st.set_page_config(
    page_title="Agentic AI",
    page_icon="⚡",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Instrument+Serif:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background: #0e0e0f;
    color: #e8e6e0;
}
.stApp { background: #0e0e0f; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 1rem 1rem !important; max-width: 780px !important; }

/* Top bar */
.topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 0 20px 0; border-bottom: 1px solid #1e1e20; margin-bottom: 24px;
}
.topbar-left { display: flex; align-items: center; gap: 10px; }
.topbar-icon {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, #c8f060, #60d4c8);
    border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 15px;
}
.topbar-name { font-family: 'Instrument Serif', serif; font-size: 22px; color: #f0ede6; }
.topbar-status { display: flex; align-items: center; gap: 6px; font-size: 11px; color: #444; font-family: 'IBM Plex Mono', monospace; }
.status-dot { width: 6px; height: 6px; border-radius: 50%; background: #c8f060; box-shadow: 0 0 6px #c8f060; }

/* Messages */
.msg { display: flex; gap: 12px; margin-bottom: 20px; animation: fadeUp .2s ease; }
.msg-user { flex-direction: row-reverse; }
@keyframes fadeUp { from { opacity:0; transform:translateY(6px); } to { opacity:1; transform:translateY(0); } }
.msg-avatar {
    width: 30px; height: 30px; border-radius: 7px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center; margin-top: 2px; font-size: 13px;
}
.avatar-ai { background: linear-gradient(135deg, #c8f060, #60d4c8); }
.avatar-user { background: #1e1e22; border: 1px solid #2a2a2e; color: #666; font-family: 'IBM Plex Mono', monospace; font-size: 9px; font-weight: 500; }
.msg-body { max-width: 88%; display: flex; flex-direction: column; gap: 8px; }
.msg-user .msg-body { align-items: flex-end; }
.msg-bubble { padding: 11px 15px; border-radius: 14px; font-size: 14.5px; line-height: 1.65; }
.bubble-user { background: #1c1c1f; border: 1px solid #2a2a2e; color: #c8c4bc; border-bottom-right-radius: 4px; }
.bubble-ai   { background: #131315; border: 1px solid #1e1e22; color: #dedad2; border-bottom-left-radius: 4px; }

/* Tool badge */
.tool-badge {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 3px 10px; border-radius: 99px;
    font-family: 'IBM Plex Mono', monospace; font-size: 10px; font-weight: 500;
    letter-spacing: 0.05em; text-transform: uppercase; width: fit-content;
}
.badge-search { background: #0d2020; color: #60d4c8; border: 1px solid #1a3535; }
.badge-code   { background: #191d0a; color: #c8f060; border: 1px solid #2c3210; }

/* Code blocks */
.code-wrap { background: #0a0a0b; border: 1px solid #1a1a1c; border-radius: 10px; overflow: hidden; margin-top: 2px; }
.code-header { display: flex; justify-content: space-between; padding: 7px 13px; border-bottom: 1px solid #1a1a1c; font-family: 'IBM Plex Mono', monospace; font-size: 10px; color: #3a3a3e; }
.code-body   { padding: 13px; font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: #a8e060; white-space: pre; overflow-x: auto; line-height: 1.6; }
.out-body    { padding: 11px 13px; font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: #f0c060; line-height: 1.5; }
.err-body    { padding: 11px 13px; font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: #f06060; line-height: 1.5; }

/* Sources */
.sources-list { display: flex; flex-direction: column; gap: 4px; margin-top: 4px; }
.src-link { font-family: 'IBM Plex Mono', monospace; font-size: 11px; color: #60d4c8; text-decoration: none; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; display: block; }
.src-link:hover { color: #90e4d8; }
.section-lbl { font-family: 'IBM Plex Mono', monospace; font-size: 10px; color: #333; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 8px; margin-bottom: 3px; }

/* Thinking dots */
.thinking { display: flex; align-items: center; gap: 8px; font-size: 12px; color: #444; font-family: 'IBM Plex Mono', monospace; padding: 8px 0; }
.dots { display: flex; gap: 4px; }
.dots span { width: 5px; height: 5px; border-radius: 50%; background: #c8f060; animation: blink 1.2s infinite; }
.dots span:nth-child(2) { animation-delay: .2s; }
.dots span:nth-child(3) { animation-delay: .4s; }
@keyframes blink { 0%,80%,100%{opacity:.15;transform:scale(.8);} 40%{opacity:1;transform:scale(1);} }

/* Welcome */
.welcome { text-align: center; padding: 60px 20px; }
.welcome-icon { width: 60px; height: 60px; background: linear-gradient(135deg,#c8f060,#60d4c8); border-radius: 16px; display: inline-flex; align-items: center; justify-content: center; font-size: 26px; margin-bottom: 20px; }
.welcome-title { font-family: 'Instrument Serif', serif; font-size: 34px; color: #f0ede6; letter-spacing: -0.5px; line-height: 1.2; margin-bottom: 10px; }
.welcome-sub { font-size: 14px; color: #4a4a50; line-height: 1.7; max-width: 380px; margin: 0 auto 28px; }
.chips { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; max-width: 500px; margin: 0 auto; }
.chip { padding: 7px 14px; background: #131315; border: 1px solid #1e1e22; border-radius: 99px; font-size: 13px; color: #666; }

/* Input overrides */
.stTextInput > div > div > input {
    background: #131315 !important; border: 1px solid #222226 !important;
    border-radius: 12px !important; color: #d4d0c8 !important;
    font-family: 'DM Sans', sans-serif !important; font-size: 14.5px !important;
    padding: 12px 16px !important;
}
.stTextInput > div > div > input:focus { border-color: #333 !important; box-shadow: none !important; }
.stButton > button {
    background: linear-gradient(135deg,#c8f060,#60d4c8) !important;
    color: #0e0e0f !important; border: none !important; border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important; font-weight: 500 !important;
    font-size: 14px !important; padding: 11px 22px !important; transition: opacity .15s !important;
}
.stButton > button:hover { opacity: .85 !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thinking" not in st.session_state:
    st.session_state.thinking = False

# ── Helper ────────────────────────────────────
def render_result(result):
    action = result.get("action", "search")
    badge = ('<span class="tool-badge badge-search">⬡ web search</span>'
             if action == "search"
             else '<span class="tool-badge badge-code">◈ code exec</span>')

    answer_text = result.get("answer", "").replace("<", "&lt;").replace(">", "&gt;")
    html = f'{badge}<div class="msg-bubble bubble-ai">{answer_text}</div>'

    if result.get("code"):
        code = result["code"].replace("<","&lt;").replace(">","&gt;")
        html += f'<div class="code-wrap"><div class="code-header"><span>python</span><span>generated</span></div><div class="code-body">{code}</div></div>'

    if result.get("execution_output"):
        out = result["execution_output"].replace("<","&lt;").replace(">","&gt;")
        html += f'<div class="code-wrap"><div class="code-header"><span>stdout</span><span>output</span></div><div class="out-body">{out}</div></div>'

    if result.get("execution_error"):
        err = result["execution_error"].replace("<","&lt;").replace(">","&gt;")
        html += f'<div class="code-wrap"><div class="code-header"><span>stderr</span><span>error</span></div><div class="err-body">{err}</div></div>'

    if result.get("sources"):
        links = "".join([f'<a class="src-link" href="{url}" target="_blank">↗ {url}</a>' for url in result["sources"] if url])
        html += f'<div class="section-lbl">Sources</div><div class="sources-list">{links}</div>'

    return html

# ── Top bar ───────────────────────────────────
st.markdown("""
<div class="topbar">
  <div class="topbar-left">
    <div class="topbar-icon">⚡</div>
    <span class="topbar-name">Agentic AI</span>
  </div>
  <div class="topbar-status"><div class="status-dot"></div>groq · langgraph · tavily</div>
</div>
""", unsafe_allow_html=True)

# ── Messages ──────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome">
      <div class="welcome-icon">⚡</div>
      <div class="welcome-title">What can I help<br><i>you figure out?</i></div>
      <div class="welcome-sub">I search the web for current info and write &amp; run Python code to solve problems.</div>
      <div class="chips">
        <div class="chip">📰 Latest AI news</div>
        <div class="chip">📈 Bitcoin price today</div>
        <div class="chip">🧮 Compound interest</div>
        <div class="chip">🔢 Is 97 a prime?</div>
        <div class="chip">🌍 India population 2025</div>
      </div>
    </div>""", unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            txt = msg["content"].replace("<","&lt;").replace(">","&gt;")
            st.markdown(f"""
            <div class="msg msg-user">
              <div class="msg-avatar avatar-user">you</div>
              <div class="msg-body"><div class="msg-bubble bubble-user">{txt}</div></div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg">
              <div class="msg-avatar avatar-ai">⚡</div>
              <div class="msg-body">{render_result(msg["result"])}</div>
            </div>""", unsafe_allow_html=True)

    if st.session_state.thinking:
        st.markdown("""
        <div class="msg">
          <div class="msg-avatar avatar-ai">⚡</div>
          <div class="msg-body">
            <div class="thinking"><div class="dots"><span></span><span></span><span></span></div>thinking...</div>
          </div>
        </div>""", unsafe_allow_html=True)

# ── Input row ────────────────────────────────
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input("msg", placeholder="Ask anything...", label_visibility="collapsed", key="chat_input")
with col2:
    send = st.button("Send →")

if st.session_state.messages:
    if st.button("✕ Clear", key="clear"):
        st.session_state.messages = []
        st.rerun()

# ── Agent call ────────────────────────────────
if send and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})
    st.session_state.thinking = True
    st.rerun()

if st.session_state.thinking:
    try:
        from agent import run_agent
        last_q = next(m["content"] for m in reversed(st.session_state.messages) if m["role"] == "user")
        result = run_agent(last_q)
        st.session_state.messages.append({"role": "assistant", "result": result})
    except Exception as e:
        st.session_state.messages.append({"role": "assistant", "result": {
            "answer": f"Error: {str(e)}", "code": "", "execution_output": "",
            "execution_error": "", "sources": [], "action": "search"
        }})
    finally:
        st.session_state.thinking = False
        st.rerun()