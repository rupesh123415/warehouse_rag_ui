import streamlit as st
import requests
import time

API_URL = "https://rupesh1904-warehouse-rag-backend.hf.space/ask"

st.set_page_config(page_title="Warehouse AI Assistant", page_icon="🚛", layout="wide")

# Professional CSS with refined color scheme
st.markdown(
    """
    <style>
    /* Main styling */
    .main {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem auto;
        max-width: 900px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    /* Header styling */
    .header {
        text-align: center;
        margin-bottom: 2rem;
        padding: 1.5rem;
        background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
        border-radius: 10px;
        color: white;
    }
    
    /* Chat containers */
    .chat-container {
        padding: 15px;
    }
    
    /* Chat bubbles */
    .user-bubble {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 0px 18px;
        margin: 12px 0;
        text-align: right;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        max-width: 80%;
        margin-left: auto;
    }
    
    .bot-bubble {
        background: linear-gradient(135deg, #ecf0f1 0%, #f5f7f9 100%);
        color: #2c3e50;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 0px;
        margin: 12px 0;
        text-align: left;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        max-width: 80%;
        border: 1px solid #e0e7ee;
    }
    
    /* Labels */
    .user-label {
        color: #3498db;
        font-weight: 600;
        text-align: right;
        margin-bottom: 4px;
        font-size: 0.85rem;
        padding-right: 10px;
    }
    
    .bot-label {
        color: #7f8c8d;
        font-weight: 600;
        text-align: left;
        margin-bottom: 4px;
        font-size: 0.85rem;
        padding-left: 10px;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: #f8f9fa;
        border-right: 1px solid #e0e7ee;
    }
    
    /* Button styling */
    .stButton button {
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: background-color 0.2s;
    }
    
    .stButton button:hover {
        background-color: #2980b9;
    }
    
    /* Input styling */
    .stChatInput {
        border-radius: 8px;
        border: 1px solid #e0e7ee;
    }
    
    /* Divider styling */
    .stDivider {
        border-color: #e0e7ee;
    }
    
    /* Info box styling */
    .stInfo {
        background-color: #e8f4fc;
        border-left: 4px solid #3498db;
    }
    
    /* Sample question buttons */
    .sample-question {
        width: 100%;
        text-align: left;
        margin-bottom: 0.5rem;
        background-color: #e8f4fc;
        border: 1px solid #3498db;
        color: #2c3e50;
    }
    
    .sample-question:hover {
        background-color: #d1e9f8;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Professional header
st.markdown(
    """
    <div class="header">
        <h1 style='margin: 0; font-size: 2.2rem; font-weight: 700;'>🚛 Warehouse AI Assistant</h1>
        <p style='margin: 0.5rem 0 0; font-size: 1.1rem; opacity: 0.9;'>Intelligent Logistics & Inventory Management</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Session state for messages
if "messages" not in st.session_state:
    st.session_state["messages"] = []
    
# Session state for sample question trigger
if "sample_question_trigger" not in st.session_state:
    st.session_state["sample_question_trigger"] = None

# Function to handle sample question selection
def handle_sample_question(question):
    st.session_state["sample_question_trigger"] = question

# Sidebar with additional options
with st.sidebar:
    st.header("Options")
    
    # Clear conversation button
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state["messages"] = []
        st.session_state["sample_question_trigger"] = None
        st.rerun()
    
    st.divider()
    
    st.header("Sample Questions")
    
    # Sample questions that users can click on
    sample_questions = [
        "What is an ASN?",
        "How to manage inventory?",
        "What is order picking?",
        "Explain warehouse safety procedures",
        "What is stock rotation?"
    ]
    
    for question in sample_questions:
        if st.button(question, key=question, use_container_width=True):
            handle_sample_question(question)
    
    st.divider()
    
    st.header("About")
    st.info("""
    This AI assistant specializes in warehouse-related queries including:
    - ASN (Advanced Shipping Notice)
    - Inventory management
    - Order processing
    - Stock management
    - Warehouse operations
    - Logistics and supply chain
    """)

# Main chat container
with st.container():
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-label'>You</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='user-bubble'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-label'>AI Assistant</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='bot-bubble'>{msg['content']}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Check if a sample question was triggered
if st.session_state["sample_question_trigger"]:
    user_input = st.session_state["sample_question_trigger"]
    st.session_state["sample_question_trigger"] = None
    
    # Add user message
    st.session_state["messages"].append({"role": "user", "content": user_input})
    
    # Get AI response
    with st.spinner("Processing your query..."):
        try:
            response = requests.post(API_URL, json={"question": user_input}, timeout=10)
            if response.status_code == 200:
                answer = response.json().get("answer", "I couldn't find a specific answer to your question. Could you please provide more details?")
            elif response.status_code == 500:
                # Handle 500 error specifically
                try:
                    # Try to parse as JSON first
                    error_data = response.json()
                    answer = error_data.get("answer", "Token Limit Reached, Please wait for few Minutes!")
                except:
                    # If not JSON, use the text response
                    answer = "Token Limit Reached, Please wait for few Minutes!"
            else:
                answer = f"Error: Received status code {response.status_code}"
        except requests.exceptions.Timeout:
            answer = "The request timed out. Please try again."
        except requests.exceptions.ConnectionError:
            answer = "Connection error. Please check your internet connection."
        except Exception as e:
            answer = f"An unexpected error occurred: {str(e)}"
    
    # Add AI response
    st.session_state["messages"].append({"role": "ai", "content": answer})
    st.rerun()

# Regular chat input
user_input = st.chat_input("Type your warehouse question...")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})

    with st.spinner("Processing your query..."):
        try:
            response = requests.post(API_URL, json={"question": user_input}, timeout=10)
            if response.status_code == 200:
                answer = response.json().get("answer", "I couldn't find a specific answer to your question. Could you please provide more details?")
            elif response.status_code == 500:
                # Handle 500 error specifically
                try:
                    # Try to parse as JSON first
                    error_data = response.json()
                    answer = error_data.get("answer", "Token Limit Reached, Please wait for few Minutes!")
                except:
                    # If not JSON, use the text response
                    answer = "Token Limit Reached, Please wait for few Minutes!"
            else:
                answer = f"Error: Received status code {response.status_code}"
        except requests.exceptions.Timeout:
            answer = "The request timed out. Please try again."
        except requests.exceptions.ConnectionError:
            answer = "Connection error. Please check your internet connection."
        except Exception as e:
            answer = f"An unexpected error occurred: {str(e)}"

    # Typing effect
    bot_reply = ""
    placeholder = st.empty()
    for char in answer:
        bot_reply += char
        time.sleep(0.01)  # typing speed
        placeholder.markdown(
            f"<div class='bot-label'>AI Assistant</div><div class='bot-bubble'>{bot_reply}</div>",
            unsafe_allow_html=True
        )
    st.session_state["messages"].append({"role": "ai", "content": answer})
    st.rerun()