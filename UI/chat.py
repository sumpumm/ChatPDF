import streamlit as st
from my_llm import response_generator
from database import *
from API.api_utils import *
from login import login_ui

def chat(token: str, session_id: str):
    # Check if the user is logged in based on the presence of token
    if "loggedin" not in st.session_state:
        st.session_state.loggedin = token is not None

    current_token = token
    current_session_id = session_id

    if st.session_state.loggedin:
        st.title("ChatPDF")
        st.header("Your online AI assistance")
        st.sidebar.header("""
                        ChatPDF!
                        A platform to interact with your PDF files
                        """)

        # Logout functionality
        if st.sidebar.button("Logout"):
            response = api_user_logout(current_token)
            st.warning(response)
            st.session_state.loggedin = False
            st.session_state.token = None  # Reset token on logout
            st.session_state.session_id = None  # Reset session_id on logout
            st.rerun()  # Rerun to trigger a reset of the app

        # File upload logic
        if "file_path" not in st.session_state:
            st.session_state.file_path = None

        uploaded_file = st.sidebar.file_uploader("Upload your pdf file here")
        if uploaded_file is not None:
            if st.sidebar.button("Upload"):
                with st.spinner("Uploading...."):
                    response, st.session_state.file_path = upload_file(uploaded_file)
                    if "success" in response:
                        st.success(response['success'])
                    else:
                        st.error(response['error'])

        # Chat options
        temperature = st.sidebar.slider("Select temperature value", min_value=0.0, max_value=1.0, value=0.8, step=0.1)
        top_k = st.sidebar.slider("Top K value", min_value=2, max_value=5, value=2, step=1)
        user_prompt = st.sidebar.text_input("Give prompt")

        # Conversation history in session state
        if "conversations" not in st.session_state:
            st.session_state.conversations = [{"role": "assistant", "content": "Hello, how may I help you today?"}]

        # Display conversations
        for conversation in st.session_state.conversations:
            with st.chat_message(conversation['role']):
                st.markdown(conversation['content'])

        # User input handling
        question = st.chat_input("Say something")

        if question:
            # Update conversation in session state
            st.session_state.conversations.append({"role": "user", "content": question})
            st.chat_message("user").markdown(question)

            with st.spinner("AI is thinking...."):
                response, session_id = api_response(token,st.session_state.file_path, question, current_session_id, temperature, top_k, user_prompt)
                st.session_state.conversations.append({"role": "assistant", "content": response})
                st.chat_message("assistant").write_stream(response_generator(response))

    else:
        # If not logged in, show the login UI
        login_ui()
