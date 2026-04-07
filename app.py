import streamlit as st
import openai

st.title("AI Prompt Tester")

api_key = st.text_input("Enter your API Key", type="password")

system_prompt = st.text_area(
    "Prompt",
    value="You are a helpful assistant.",
    height=150
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_text = st.chat_input("Write your message")

if api_key and user_text:
    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://inference.bunyan.ai"
    )

    st.session_state.messages.append({"role": "user", "content": user_text})

    messages = [{"role": "system", "content": system_prompt}]
    messages += st.session_state.messages

    response = client.chat.completions.create(
        model="saudi/llama-4-maverick-17b-128e-instruct",
        messages=messages
    )

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})

    st.rerun()