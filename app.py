import streamlit as st
from transformers import pipeline

# Streamlit settings
st.set_page_config(page_title="Finance Chatbot", page_icon="💹")
st.title("💹 Finance AI Chatbot")
st.write("Ask anything about finance, investing, or money management!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Load Hugging Face chatbot pipeline
@st.cache_resource(show_spinner=False)
def load_model():
    return pipeline("text-generation", model="tiiuae/falcon-7b-instruct", device=0)

chatbot = load_model()

# User input
user_input = st.chat_input("Type your finance question here...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get AI response
    response = chatbot(user_input, max_length=200, do_sample=True)[0]['generated_text']
    st.session_state.messages.append({"role": "assistant", "content": response})

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])
