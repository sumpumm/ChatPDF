import streamlit as st
from login import login_ui
from chat import chat
from register import register_ui


if "token" not in st.session_state:
    st.session_state.token = None

if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "loggedin" not in st.session_state:
    st.session_state.loggedin = False

if "logout_clicked" not in st.session_state:
    st.session_state.logout_clicked = False

if "register_clicked" not in st.session_state:
    st.session_state.register_clicked = False

if st.session_state.logout_clicked:
    # Reset all session variables
    st.session_state.token = None
    st.session_state.session_id = None
    st.session_state.loggedin = False
    st.session_state.logout_clicked = False
    st.rerun() 

if st.session_state.register_clicked:
    register_ui()
    st.stop()

if not st.session_state.loggedin:
    result = login_ui()  
    if result is not None:
        st.session_state.token, st.session_state.session_id = result
        st.session_state.loggedin = True
        st.rerun()  
else:
    chat(st.session_state.token, st.session_state.session_id)


    