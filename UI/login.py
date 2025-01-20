import streamlit as st
from API.api_utils import api_user_login

def login_ui():    
    st.title("Login")
    username=st.text_input("Username",placeholder="Enter username")
    password=st.text_input("Password",placeholder="Enter password",type="password")

    if st.button("Login"):
        with st.spinner("Uploading..."):
                response_token,response_session_id,response_result=api_user_login(username,password)
                if response_result:
                    return response_token,response_session_id
                else:
                    st.error("Incorrect Username/Password")
                    return None,None
                 
                    
                