import streamlit as st
import uuid
import time
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, MessagesState
from langchain_core.messages import HumanMessage, AIMessage

# ── ENV ───────────────────────────────────────────────────────────────────────

from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env", override=True)

api_key = os.getenv("GROQ_API_KEY")
api_key = st.secrets.get("GROQ_API_KEY", None)

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Zeno AI",
    page_icon="❄️",
)

# ── CSS (exact original colors + animations) ──────────────────────────────────
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: #DFF1F1;
}
[data-testid="stSidebar"] {
    background-color: #B7BDF7;
}
[data-testid="stHeader"] {
    background: #BBD5DA;
}

/* Chat bubbles */
.user-msg {
    background: #2563eb;
    color: white;
    padding: 12px 18px;
    border-radius: 15px;
    margin: 8px 0;
    width: fit-content;
    margin-left: auto;
    animation: fadeIn 0.4s ease-in-out;
    max-width: 75%;
    word-break: break-word;
    white-space: pre-wrap;
}

.bot-msg {
    background: #e2e8f0;
    color: black;
    padding: 12px 18px;
    border-radius: 15px;
    margin: 8px 0;
    width: fit-content;
    max-width: 75%;
    word-break: break-word;
    white-space: pre-wrap;
    animation: fadeIn 0.4s ease-in-out;
}

/* Typing animation */
.typing {
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 12px 18px;
    background: #e2e8f0;
    border-radius: 15px;
    width: fit-content;
}
.typing span {
    height: 8px;
    width: 8px;
    background: gray;
    border-radius: 50%;
    display: inline-block;
    animation: bounce 1.4s infinite;
}
.typing span:nth-child(2) { animation-delay: 0.2s; }
.typing span:nth-child(3) { animation-delay: 0.4s; }

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes bounce {
    0%, 80%, 100% { transform: scale(0); }
    40%           { transform: scale(1); }
}

/* Sidebar elements */
[data-testid="stSidebar"] * {
    color: #1a1a2e !important;
}
.stButton > button {
    width: 100%;
    border-radius: 8px;
}

/* Chat input */
[data-testid="stChatInput"] textarea {
    background: white;
}
</style>
""", unsafe_allow_html=True)


# ── LLM + GRAPH (cached) ──────────────────────────────────────────────────────
if st.button("🔄 Reload App"):
    st.cache_resource.clear()
    st.rerun()
def get_graph(api_key: str, model_name: str):
    llm = ChatGroq(groq_api_key=api_key, model_name=model_name)

    def chatbot_node(state: MessagesState):
        return {"messages": [llm.invoke(state["messages"])]}

    g = StateGraph(MessagesState)
    g.add_node("chatbot", chatbot_node)
    g.set_entry_point("chatbot")
    g.set_finish_point("chatbot")
    return g.compile(checkpointer=InMemorySaver())


# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Controls")

    active_key = api_key

    model_choice = st.selectbox("Model", [
        "llama-3.1-8b-instant",
        "llama-3.3-70b-versatile",
        "mixtral-8x7b-32768",
    ])

    if st.button("🆕 New Chat"):
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.write("Session ID:")
    st.code(st.session_state.thread_id[:8])


# ── HEADER ────────────────────────────────────────────────────────────────────
st.title("❄️ Zeno AI")
st.caption("Here to help, anytime ✨")


# ── CHAT DISPLAY ──────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    is_human = isinstance(msg, HumanMessage)
    content  = msg.content.replace("<", "&lt;").replace(">", "&gt;")
    css_cls  = "user-msg" if is_human else "bot-msg"
    st.markdown(f'<div class="{css_cls}">{content}</div>', unsafe_allow_html=True)


# ── INPUT ─────────────────────────────────────────────────────────────────────
if not active_key:
    st.info("Enter your GROQ API key in the sidebar to start chatting.", icon="🔑")
else:
    user_input = st.chat_input("Type your message...")

    if user_input and user_input.strip():
        human_msg = HumanMessage(content=user_input)
        st.session_state.messages.append(human_msg)

        safe_input = user_input.replace("<", "&lt;").replace(">", "&gt;")
        st.markdown(f'<div class="user-msg">{safe_input}</div>', unsafe_allow_html=True)

        # Typing indicator
        typing_ph = st.empty()
        typing_ph.markdown("""
        <div class="typing">
            <span></span><span></span><span></span>
        </div>
        """, unsafe_allow_html=True)

        # LLM call
        app_graph = get_graph(active_key, model_choice)
        config    = {"configurable": {"thread_id": st.session_state.thread_id}}

        try:
            response  = app_graph.invoke(
                {"messages": st.session_state.messages},
                config=config
            )
            bot_reply = response["messages"][-1].content
        except Exception as e:
            bot_reply = f"[error] {e}"

        typing_ph.empty()

        # Typewriter effect
        display_text = ""
        msg_ph = st.empty()
        for char in bot_reply:
            display_text += char
            safe_display = display_text.replace("<", "&lt;").replace(">", "&gt;")
            msg_ph.markdown(
                f'<div class="bot-msg">{safe_display}</div>',
                unsafe_allow_html=True
            )
            time.sleep(0.008)

        st.session_state.messages.append(AIMessage(content=bot_reply))
        st.rerun()


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("Simple 🧩 Smart 🧠 Helpful 🌟")
