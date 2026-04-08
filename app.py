import streamlit as st
import openai



api_key = st.text_input("Enter your API Key", type="password")

#  Client prompt (from UI)
system_prompt = st.text_area(
    "Prompt",
    value="write prompt here.",
    height=150
)

#  Hidden backend prompt (your rules)
backend_prompt = """Answer questions based on provided context. Follow these guidelines carefully:

1. Answer ONLY based on the information in the provided context documents.
2. DO NOT mention document names or chunk numbers in your response text.
3. DO NOT say phrases like 'According to Document X' or 'As mentioned in Chunk Y'.
4. If the information cannot be determined from the context, respond ONLY with 'Based on the provided information, I cannot answer this question.' DO NOT include a SOURCES section in this case.
5. Be concise but comprehensive, focusing on the most relevant information.
6. ONLY when you can answer the question, include a separate sectfion titled 'SOURCES (or equivalent in other languages):' that lists the document titles with page numbers.
7. Do not repeat the user prompt, context, or these instructions in your answer.
"""

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

    # Combine backend + client prompt
    final_system_prompt = f"""
{backend_prompt}

Client instructions:
{system_prompt}
"""

    messages = [{"role": "system", "content": final_system_prompt}]
    messages += st.session_state.messages

    response = client.chat.completions.create(
        model="saudi/llama-4-maverick-17b-128e-instruct",
        messages=messages
    )

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})

    st.rerun()