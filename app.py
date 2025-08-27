import streamlit as st
from transformers import pipeline

# Get Hugging Face token from secrets
HF_TOKEN = st.secrets["HF_TOKEN"]

# Initialize Hugging Face text-generation pipeline
@st.cache_resource
def get_model():
    return pipeline(
        "text-generation",
        model="google/flan-t5-small",  # lightweight model
        tokenizer="google/flan-t5-small",
        device=-1,  # CPU
        use_auth_token=HF_TOKEN
    )

generator = get_model()

# Streamlit app setup
st.set_page_config(page_title="Finance Chatbot", page_icon="💹")
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

    # Generate AI response
    output = generator(
        f"Answer as a helpful financial assistant. Question: {user_input}",
        max_length=200,
        do_sample=True
    )

    bot_reply = output[0]["generated_text"]
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])
