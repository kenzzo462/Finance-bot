import streamlit as st
from transformers import pipeline

# Page setup
st.set_page_config(page_title="Finance AI Chatbot", page_icon="💹")
st.title("💹 Finance AI Chatbot")
st.write("Ask anything about finance, investing, or money management!")

# Initialize Hugging Face text-generation pipeline
@st.cache_resource  # caches the model so it doesn't reload every input
def load_model():
    return pipeline("text-generation", model="facebook/opt-1.3b")  # lightweight model

generator = load_model()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# User input
user_input = st.chat_input("Type your finance question here...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate bot response
    output = generator(f"Answer as a helpful financial assistant. Question: {user_input}", 
                       max_length=200, do_sample=True, top_p=0.9)
    bot_reply = output[0]['generated_text'].split("Question:")[-1].strip()
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])
        
