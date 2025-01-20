# Main application code
import streamlit as st
from login import login_ui
from chat import chat

if "token" not in st.session_state:
    st.session_state.token = None

if "session_id" not in st.session_state:
    st.session_state.session_id = None

if st.session_state.token is None:
    result = login_ui()  
    if result is not None: 
        st.session_state.token, st.session_state.session_id = result
else:
    token = st.session_state.token
    session_id = st.session_state.session_id
    chat(token, session_id)  

