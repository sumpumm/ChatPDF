import streamlit as st
import os
from pypdf import PdfWriter,PdfReader
from my_llm import RAG,response_generator
from langchain.memory import ConversationBufferMemory
import secrets
from langchain_community.chat_message_histories import (
    PostgresChatMessageHistory,
)



st.title("ChatPDF")
st.header("Your online Ai assistance")
st.sidebar.header("""
                  ChatPDF!
                  A platform to interact with your PDF files 
                  """)


# WOrking with files
uploaded_files=st.sidebar.file_uploader("Upload your pdf file here",accept_multiple_files=True,type="pdf")
save_directory="uploaded_PDFs"
merged_file_name="merged_output"

if uploaded_files:
    if(len(uploaded_files)>1):
        #logic for multiple files handling
        writer=PdfWriter()
        for uploaded_file in uploaded_files:
            reader=PdfReader(uploaded_file)
            for page in reader.pages:
                writer.add_page(page)
            merged_file_name+="_"+ uploaded_file.name.split('.')[0]
        file_path = os.path.join(save_directory, merged_file_name + ".pdf")
        
        with open(file_path, "wb") as output_file:
            writer.write(output_file)
            
    else:
        os.makedirs(save_directory,exist_ok=True) 
        file_path=os.path.join(save_directory,uploaded_files[0].name)
        #this saves the file
        with open(file_path, "wb") as f:
            f.write(uploaded_files[0].getbuffer())


if "session_id" not in st.session_state:
    st.session_state.session_id=secrets.token_hex(16)
    


if "postgres_chat" not in st.session_state:
    st.session_state.postgres_chat=PostgresChatMessageHistory(
    connection_string="postgresql://postgres:sumpumm@localhost/chat_history",
    session_id=st.session_state.session_id,)

history=st.session_state.postgres_chat
         
if "conversations" not in st.session_state:
    st.session_state.conversations=[{"role":"assistant","content":"Hello, how may I help you today?"}]
    history.add_ai_message("Hello, how may I help you today?")

if "chat_memory" not in st.session_state:
        st.session_state.chat_memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )

# Access the memory from session state
memory = st.session_state.chat_memory

for conversation in st.session_state.conversations:
    with st.chat_message(conversation['role']):
        st.markdown(conversation['content'])

question=st.chat_input("Say something")


if question:
    #this will update the consersation in session state
    st.session_state.conversations.append({"role":"user","content": question})
    st.chat_message("user").markdown(question)
    history.add_user_message(question)
    
    
    response=RAG(question,file_path,memory)
    
    st.session_state.conversations.append({"role":"assistant","content": response})
    st.chat_message("assistant").write_stream(response_generator(response))
    history.add_ai_message(response)
    
    



