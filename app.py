import streamlit as st
from transformers import pipeline

# -------------------------
# Page Setup
# -------------------------
st.set_page_config(page_title="Finance Chatbot", page_icon="💹")
st.title("💹 Finance AI Chatbot")
st.write("Ask anything about finance, investing, or money management!")

# -------------------------
# Initialize chat history
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------
# Initialize HF model
# -------------------------
@st.cache_resource
def get_model():
    return pipeline("text-generation", model="google/flan-t5-small")

model = get_model()

# -------------------------
# User Input
# -------------------------
user_input = st.text_input("Type your finance question here...")

if user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Generate AI response
    prompt = f"Answer as a helpful financial assistant. Question: {user_input}"
    result = model(prompt, max_length=150, do_sample=True)
    bot_reply = result[0]['generated_text']
    
    # Append bot message
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# -------------------------
# Display chat
# -------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**Bot:** {msg['content']}")
