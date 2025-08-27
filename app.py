import streamlit as st
from openai import OpenAI

# 🔑 Replace with your OpenAI API key
OPENAI_API_KEY = "your_api_key_here"

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Streamlit App
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

# User input
user_input = st.chat_input("Type your finance question here...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get AI response
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages
    )

    bot_reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])
