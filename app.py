import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Configure the Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro-latest")

st.set_page_config(page_title="🧠 Mental Health Chatbot", page_icon="🧠")
st.title("🧠 AI Mental Health Chatbot")
st.write("💬 Chat with an AI therapist about your feelings, emotions, stress, or mental well-being.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm here to support your mental well-being. How are you feeling today?"}
    ]

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("How are you feeling today?")

if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Mental health tailored response
    prompt = f"""
    You are a compassionate mental health AI assistant. Respond empathetically to the user's input.

    User: {user_input}

    Your response should include:
    - Emotional validation
    - Supportive advice or coping strategies
    - When to seek help from a professional
    - Encouraging tone throughout
    """

    response = model.generate_content(prompt).text.strip()

    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(response)
