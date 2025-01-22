import streamlit as st
from API.api_utils import api_user_logout, api_response, upload_file
from my_llm import response_generator
import time

def chat(token: str, session_id: str):
    st.title("ChatPDF")
    st.header("Your online AI assistant")
    st.sidebar.header("ChatPDF! A platform to interact with your PDF files")


    if st.sidebar.button("Logout"):
        with st.spinner("Logging out..."):
            response = api_user_logout(token)
            st.success(response)
            st.session_state.logout_clicked = True  
            time.sleep(5)
            st.rerun() 

    
    uploaded_file = st.sidebar.file_uploader("Upload your PDF file here")
    if uploaded_file and st.sidebar.button("Upload"):
        with st.spinner("Uploading..."):
            response, st.session_state.file_path = upload_file(uploaded_file)
            if "success" in response:
                st.success(response['success'])
            else:
                st.error(response.get('error', 'Unknown error occurred'))

    
    temperature = st.sidebar.slider("Select temperature value", 0.0, 1.0, 0.8, 0.1)
    top_k = st.sidebar.slider("Top K value", 2, 5, 2, 1)
    user_prompt = st.sidebar.text_input("Give prompt")

    
    if "conversations" not in st.session_state:
        st.session_state.conversations = [{"role": "assistant", "content": "Hello, how may I help you today?"}]

    for conversation in st.session_state.conversations:
        with st.chat_message(conversation['role']):
            st.markdown(conversation['content'])

    question = st.chat_input("Say something")
    if question:
        st.session_state.conversations.append({"role": "user", "content": question})
        st.chat_message("user").markdown(question)

        with st.spinner("AI is thinking..."):
            response, session_id = api_response(token, st.session_state.file_path, question, session_id, temperature, top_k, user_prompt)
            if session_id is None:
                st.session_state.logout_clicked = True 
                st.warning("Token expired. You have been logged out!") 
                time.sleep(5)
                st.rerun()
            st.session_state.conversations.append({"role": "assistant", "content": response})
            st.chat_message("assistant").write_stream(response_generator(response))
        st.rerun()