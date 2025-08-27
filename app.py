import streamlit as st
import requests

# Hugging Face API setup
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct"
headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Streamlit App
st.set_page_config(page_title="Finance Chatbot", page_icon="💹")
st.title("💹 Finance AI Chatbot")
st.write("Ask anything about finance, investing, or money management!")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Type your finance question here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    prompt = (
        "You are a helpful financial assistant. "
        "Only answer finance-related questions in simple, clear language. "
        f"User: {user_input}\nAssistant:"
    )

    output = query({"inputs": prompt})
    bot_reply = output[0]["generated_text"].split("Assistant:")[-1].strip()

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])
    
