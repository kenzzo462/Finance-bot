import streamlit as st
import requests

# Page setup
st.set_page_config(page_title="Finance AI Chatbot", page_icon="💹")
st.title("💹 Finance AI Chatbot")
st.write("Ask anything about finance, investing, or money management!")

# Hugging Face API key from secrets
HF_API_KEY = st.secrets["HF_API_KEY"]
API_URL = "https://api-inference.huggingface.co/models/facebook/opt-1.3b"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# User input
user_input = st.chat_input("Type your finance question here...")

def query_hf(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()[0]['generated_text']
    else:
        return f"Error: {response.status_code} - {response.text}"

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call Hugging Face API
    prompt = f"Answer as a helpful financial assistant. Question: {user_input}"
    bot_reply = query_hf({"inputs": prompt, "parameters": {"max_new_tokens": 150}})
    
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])
        
