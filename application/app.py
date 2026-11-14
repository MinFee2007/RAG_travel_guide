import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from authentication import sign_in, sign_up
from rag import respond_rag

# Config streamlit page
st.set_page_config(page_title="Travel Assistant RAG", layout="centered")

# Initialize session state for authentication and chat history
if "user" not in st.session_state:
    st.session_state.user = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# AUTHENTICATION INTERFACE (LOGIN / REGISTER)
if not st.session_state.user:
    # Title and action selector
    st.title("Log in to the Travel Assistant system")
    auth_mode = st.radio("Select action:", ["Sign in", "Sign up"])

    # Input
    email = st.text_input("Email",type='email')
    password = st.text_input("Password", type="password")

    # Handle submit
    if st.button("Submit"):
        if auth_mode == "Sign in":
            res = sign_in(email, password)
            if "idToken" in res:
                st.session_state.user = res["email"]
                st.success("Sign in successfully!")
                st.rerun()
            else:
                st.error(f"Sign in failed: {res.get('error', {}).get('message', 'Unknown error')}")
        else:
            res = sign_up(email, password)
            if "idToken" in res:
                st.success("Registration successful! Please switch to the Login tab..")
            else:
                st.error(f"Sign in failed: {res.get('error', {}).get('message', 'Unknown error')}")

# RAG CHAT INTERFACE (AFTER LOGGING IN)
else:
    st.sidebar.title(f"Hello {st.session_state.user}")

    # Handle log out button
    if st.sidebar.button("Log out"):
        st.session_state.user = None
        st.session_state.messages = []
        st.rerun()

    st.title("Smart Travel Assistant")

    # Show chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Get user prompt
    if prompt := st.chat_input("What would you like to know about your travel destination??"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Handle assistant's chat UI
        with st.chat_message("assistant"):
            with st.spinner("Finding information..."):
                try:
                    # Get response here
                    answer, sources = respond_rag(prompt)
                    st.markdown(answer)
                    
                    # Display source citations and similarity levels in the expander
                    with st.expander("View source material and similarity"):
                        for src in sources:
                            st.write(f"- **ID:** {src['id']} | **Score:** {src['score']:.4f} | **Source:** {src['source']}")

                    # Show the AI response on Streamlit app
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                
                except Exception as e:
                    error_msg = f"An error occurred while connecting to the Ollama server or processing RAG: {e}"
                    st.error(error_msg)