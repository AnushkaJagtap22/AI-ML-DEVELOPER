import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
)

load_dotenv()

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="AI ChatBot",
    page_icon="🤖",
    layout="centered",
)

# -------------------------------------------------
# Custom CSS
# -------------------------------------------------
st.markdown("""
<style>

/* Background */
.stApp{
    background: linear-gradient(135deg,#0f172a,#1e293b,#312e81,#4c1d95);
    background-size:400% 400%;
}

/* Main Container */
.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
    max-width:900px;
}

/* Title */
.main-title{
    text-align:center;
    font-size:48px;
    font-weight:800;
    background:linear-gradient(90deg,#38bdf8,#22d3ee,#818cf8,#ec4899);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    margin-bottom:5px;
}

.subtitle{
    text-align:center;
    color:#d1d5db;
    font-size:18px;
    margin-bottom:30px;
}

/* Card */
.card{
    background:rgba(255,255,255,0.08);
    padding:25px;
    border-radius:20px;
    backdrop-filter:blur(10px);
    border:1px solid rgba(255,255,255,.15);
    margin-bottom:25px;
}

/* Button */
.stButton>button{
    width:100%;
    border:none;
    border-radius:12px;
    padding:12px;
    font-size:18px;
    font-weight:bold;
    color:white;
    background:linear-gradient(90deg,#2563eb,#7c3aed,#ec4899);
    transition:.3s;
}

.stButton>button:hover{
    transform:scale(1.02);
    box-shadow:0 0 20px rgba(124,58,237,.5);
}

/* Selectbox Label */
.stSelectbox label{
    color:white !important;
    font-weight:bold;
    font-size:17px;
}

/* Chat Bubbles */
.user-msg{
    background:#16a34a;
    color:white;
    padding:14px;
    border-radius:18px;
    margin:10px 0;
}

.bot-msg{
    background:#2563eb;
    color:white;
    padding:14px;
    border-radius:18px;
    margin:10px 0;
}

/* Chat Input */
.stChatInput{
    border-radius:20px;
}

/* Scrollbar */
::-webkit-scrollbar{
    width:8px;
}

::-webkit-scrollbar-thumb{
    background:#7c3aed;
    border-radius:20px;
}

::-webkit-scrollbar-track{
    background:#1e293b;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Header
# -------------------------------------------------
st.markdown(
    "<h1 class='main-title'>🤖 AI ChatBot</h1>",
    unsafe_allow_html=True,
)

st.markdown(
    "<p class='subtitle'>Powered by Mistral AI</p>",
    unsafe_allow_html=True,
)

# -------------------------------------------------
# Model
# -------------------------------------------------
model = init_chat_model(
    "mistral-small-latest",
    temperature=0.9,
)

# -------------------------------------------------
# Session State
# -------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "started" not in st.session_state:
    st.session_state.started = False

# -------------------------------------------------
# Mood Selection
# -------------------------------------------------
if not st.session_state.started:

    st.markdown(
        """
        <div class='card'>
        <h2 style='text-align:center;color:white;'>
        🎭 Choose Your AI Mood
        </h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    mood = st.selectbox(
        "",
        ["Funny 😂", "Angry 😡", "Neutral 🙂"],
    )

    if st.button("🚀 Start Chat"):

        if mood.startswith("Funny"):
            prompt = "You are a very funny AI agent."

        elif mood.startswith("Angry"):
            prompt = "You are a very angry AI agent."

        else:
            prompt = "You are a very neutral AI agent."

        st.session_state.messages = [
            SystemMessage(content=prompt)
        ]

        st.session_state.started = True
        st.rerun()

# -------------------------------------------------
# Chat Screen
# -------------------------------------------------
else:

    for message in st.session_state.messages:

        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(
                    f"<div class='user-msg'>{message.content}</div>",
                    unsafe_allow_html=True,
                )

        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(
                    f"<div class='bot-msg'>{message.content}</div>",
                    unsafe_allow_html=True,
                )

    user_input = st.chat_input("Type your message...")

    if user_input:

        with st.chat_message("user"):
            st.markdown(
                f"<div class='user-msg'>{user_input}</div>",
                unsafe_allow_html=True,
            )

        st.session_state.messages.append(
            HumanMessage(content=user_input)
        )

        response = model.invoke(st.session_state.messages)

        with st.chat_message("assistant"):
            st.markdown(
                f"<div class='bot-msg'>{response.content}</div>",
                unsafe_allow_html=True,
            )

        st.session_state.messages.append(
            AIMessage(content=response.content)
        )