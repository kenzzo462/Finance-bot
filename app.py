# app.py
import streamlit as st
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

st.set_page_config(page_title="Finance Chatbot", page_icon="💹")
st.title("💹 Finance AI Chatbot")
st.write("Ask anything about finance, investing, or money management!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system",
         "content": (
             "You are a helpful financial assistant. "
             "Only answer finance-related questions in simple, clear language. "
             "Politely redirect if asked non-finance questions."
         )}
    ]

# Load Hugging Face model (causal LM for chat)
@st.cache_resource
def load_model():
    model_name = "tiiuae/falcon-7b-instruct"  # open-weight model, adjust if needed
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
    return generator

generator = load_model()

# User input
user_input = st.chat_input("Type your finance question here...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Prepare context for model
    context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    response = generator(context, max_length=300, do_sample=True, temperature=0.7)
    bot_reply = response[0]['generated_text'].split("assistant:")[-1].strip()

    # Add assistant reply to session
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])
