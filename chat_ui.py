import streamlit as st
import requests
import time

API_URL = "https://rupesh1904-warehouse-rag-backend.hf.space/ask"

st.set_page_config(page_title="Warehouse AI Assistant", page_icon="🚛", layout="wide")

# Custom CSS for premium look
st.markdown(
    """
    <style>
    .chat-container {
        max-width: 800px;
        margin: auto;
        padding: 10px;
    }
    .user-bubble {
        background: linear-gradient(135deg, #0078d4, #005a9e);
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 0px 18px;
        margin: 8px 0;
        text-align: right;
        box-shadow: 0px 3px 6px rgba(0,0,0,0.25);
    }
    .bot-bubble {
        background: linear-gradient(135deg, #f1f3f4, #e4e7eb);
        color: #222;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 0px;
        margin: 8px 0;
        text-align: left;
        box-shadow: 0px 3px 6px rgba(0,0,0,0.15);
    }
    .user-label {
        color: #0078d4;
        font-weight: bold;
        text-align: right;
        margin-bottom: -6px;
    }
    .bot-label {
        color: #444;
        font-weight: bold;
        text-align: left;
        margin-bottom: -6px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Unique premium heading
st.markdown(
    """
    <h1 style='
        text-align: center;
        background: linear-gradient(90deg, #0078d4, #00c6ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 42px;
        font-weight: 900;
        letter-spacing: 2px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.25);
        margin-bottom: 15px;
    '>
        🚛 Warehouse AI Assistant
    </h1>
    <p style='text-align:center; color: #567; font-size: 18px; margin-top:-10px;'>
        Smart. Fast. Warehouse-ready.
    </p>
    """,
    unsafe_allow_html=True
)

# Session state for messages
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Chat history container
with st.container():
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-label'>You</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='user-bubble'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-label'>AI</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='bot-bubble'>{msg['content']}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Type your warehouse question...")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})

    with st.spinner("AI is thinking..."):
        try:
            response = requests.post(API_URL, json={"question": user_input})
            if response.status_code == 200:
                answer = response.json().get("answer", "⚠️ No answer received.")
            else:
                answer = f"⚠️ Error: {response.text}"
        except Exception as e:
            answer = f"⚠️ API connection error: {str(e)}"

    # Fake typing effect
    bot_reply = ""
    placeholder = st.empty()
    for char in answer:
        bot_reply += char
        time.sleep(0.015)  # typing speed
        placeholder.markdown(
            f"<div class='bot-label'>AI</div><div class='bot-bubble'>{bot_reply}</div>",
            unsafe_allow_html=True
        )
    st.session_state["messages"].append({"role": "ai", "content": answer})
    st.rerun()
