import streamlit as st
import os
from pypdf import PdfWriter,PdfReader
from main import main,response_generator


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



