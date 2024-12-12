import streamlit as st
import os
from main import main,response_generator


st.title("ChatPDF")
st.header("Your online Ai assistance")
st.sidebar.header("""
                  Hello,Welcome to chatPDF!
                  How may I help you?
                  """)


# WOrking with files
uploaded_file=st.file_uploader("Upload your pdf file here",type="pdf")
save_directory="uploaded_PDFs"

if uploaded_file is not None:
    os.makedirs(save_directory,exist_ok=True) 
    file_path=os.path.join(save_directory,uploaded_file.name)
    
    #this saves the file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        

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
    
    response=main(question,file_path)
    
    st.session_state.conversations.append({"role":"assistant","content": response})
    st.chat_message("assistant").write_stream(response_generator(response))
    st.rerun()



