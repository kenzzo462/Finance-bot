
import streamlit as st
from huggingface_hub import InferenceClient

# Get token and model from Streamlit secrets
HF_API_KEY = st.secrets["HF_API_KEY"]
MODEL_ID = st.secrets.get("MODEL_ID", "google/flan-t5-small")

# Initialize Hugging Face Inference client
client = InferenceClient(HF_API_KEY)

# Streamlit App
st.set_page_config(page_title="Finance AI Chatbot", page_icon="💹")
st.title("💹 Finance AI Chatbot")
st.write("Ask anything about finance, investing, or money management!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# User input
user_input = st.chat_input("Type your finance question here...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Query Hugging Face model
    try:
        output = client.text_generation(
            model=MODEL_ID,
            inputs=user_input,
            max_new_tokens=150
        )
        bot_reply = output[0]["generated_text"].strip()
    except Exception as e:
        bot_reply = f"Error: {str(e)}"

    # Add assistant reply to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])
    
