import streamlit as st
from API.api_utils import api_register_user
from login import login_ui


def register_ui():    
    st.title("ChatPDF User registration")
    username=st.text_input("Username",placeholder="Enter username")
    email=st.text_input("Email",placeholder="Enter password Email address")
    full_name=st.text_input("Full Name",placeholder="Enter your full name")
    password=st.text_input("Password",placeholder="Enter password",type="password")
    password_again=st.text_input(label="Confirm Password",placeholder="Enter password again",type="password")

    if st.button(label="Submit"):
        with st.spinner("Uploading..."):
            if password==password_again:  
                response_result,response_message=api_register_user(username,email,full_name,password)
                if response_result:
                    st.success(response_message)
                else:
                    st.error(response_message)
            else:
                st.error("password doesnt match!")
      

register_ui()