import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Configure the Gemini API key
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro-latest")


# Streamlit page setup
st.set_page_config(page_title="🧠 Mental Health Chatbot", page_icon="🧠")
st.title("🧠 AI Mental Health Chatbot")
st.write("💬 Chat with an AI therapist about your feelings, emotions, stress, or mental well-being.")

# Tone selector
tone = st.selectbox("Choose the tone you prefer:", ["Empathetic", "Encouraging", "Practical", "Motivational"])

# Clear chat button
if st.button("🧹 Clear Chat"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm here to support your mental well-being. How are you feeling today?"}
    ]
    st.experimental_rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm here to support your mental well-being. How are you feeling today?"}
    ]

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("How are you feeling today?")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # Prompt to Gemini model
    prompt = f"""
    You are a compassionate mental health AI assistant. Respond in a {tone.lower()} tone to the user's message.

    Keep your response **brief and easy to read** (ideally between 30 to 50 words).

    User: {user_input}

    Your response should include:
    - Emotional validation
    - One supportive suggestion or coping strategy
    - A gentle reminder that it's okay to seek professional help
    - Maintain an encouraging tone throughout
"""

    with st.chat_message("assistant"):
        with st.spinner("Typing..."):
            response = model.generate_content(prompt).text.strip()
            st.markdown(response)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})