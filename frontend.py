import streamlit as st
from my_llm import response_generator
from config import *
from api_utils import *


st.title("ChatPDF")
st.header("Your online Ai assistance")
st.sidebar.header("""
                  ChatPDF!
                  A platform to interact with your PDF files 
                  """)

if "file_path" not in st.session_state:
    st.session_state.file_path=None
    
# WOrking with files
uploaded_file=st.sidebar.file_uploader("Upload your pdf file here")
if uploaded_file is not None:
    if st.sidebar.button("Upload"):
        with st.spinner("uploading...."):
            response,st.session_state.file_path=upload_file(uploaded_file)
            if "success" in response:
                st.success(response['success'])
            else:
                st.error(response['error'])

temperature=st.sidebar.slider("Select temperature value",min_value=0.0,max_value=1.0,value=0.8,step=0.1)
top_k=st.sidebar.slider("top_k value",min_value=2,max_value=5,value=2,step=1)

user_prompt= st.sidebar.text_input("Give prompt")

if "session_id" not in st.session_state:
    st.session_state.session_id=None
 
if "conversations" not in st.session_state:
    st.session_state.conversations=[{"role":"assistant","content":"Hello, how may I help you today?"}]
   

for conversation in st.session_state.conversations:
    with st.chat_message(conversation['role']):
        st.markdown(conversation['content'])

question=st.chat_input("Say something")

if question:
    #this will update the consersation in session state
    st.session_state.conversations.append({"role":"user","content": question})
    st.chat_message("user").markdown(question)
    
    with st.spinner("Ai is thinking...."):
        response,session_id = api_response(st.session_state.file_path,question,st.session_state.session_id,temperature,top_k,user_prompt)
        st.session_state.session_id=session_id
        st.session_state.conversations.append({"role":"assistant","content": response})
        st.chat_message("assistant").write_stream(response_generator(response))
    st.rerun()
        
        
    