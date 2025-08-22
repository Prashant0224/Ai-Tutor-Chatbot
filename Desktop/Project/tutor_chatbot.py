import streamlit as st
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Page settings
st.set_page_config(page_title="AI Tutor Chatbot", page_icon="🤖", layout="wide")

# Sidebar
with st.sidebar:
    st.title("🤖 AI Tutor")
    st.markdown("Your **personal AI tutor** for Python, ML, DL, and AI 🚀")
    if st.button("🧹 Clear Chat"):
        st.session_state.chat = genai.GenerativeModel("gemini-1.5-flash").start_chat(history=[])
        st.experimental_rerun()

st.title("💬 AI Tutor Chatbot")
st.write("Ask me anything about **Python, Machine Learning, Deep Learning, or AI** 👇")

# Initialize chat
if "chat" not in st.session_state:
    st.session_state.chat = genai.GenerativeModel("gemini-1.5-flash").start_chat(history=[])

# Chat display
chat_container = st.container()
with chat_container:
    for msg in st.session_state.chat.history:
        role = "🧑 You" if msg.role == "user" else "🤖 Tutor"
        bg_color = "#DCF8C6" if msg.role == "user" else "#F1F0F0"
        align = "right" if msg.role == "user" else "left"

        st.markdown(
            f"""
            <div style="background-color:{bg_color}; padding:10px; border-radius:10px; 
                        margin:5px; text-align:{align}; max-width:80%; display:inline-block;">
                <b>{role}:</b><br>{msg.parts[0].text}
            </div>
            """,
            unsafe_allow_html=True
        )

# User input
if prompt := st.chat_input("Type your question here..."):
    st.session_state.chat.send_message(prompt)

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant message
    with st.chat_message("assistant"):
        reply = st.session_state.chat.history[-1].parts[0].text
        st.markdown(reply)
