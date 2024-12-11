import streamlit as st
import os
from main import main


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
        

if "conversation" not in st.session_state:
    st.session_state.conversation="ChatPDF: Hello, how can I help you?\n"

st.markdown(
    f"""
    <h5>Chat</h5>
    <div style="background-color: black; color: white; padding: 10px; border-radius: 5px; height: 500px; overflow-y: auto;">
         {st.session_state.conversation.replace('\n', '<br>')}
    </div>
    """,
    unsafe_allow_html=True,
)

question=st.text_area("Ask away",placeholder="What do you want to know about the PDF",key="key_interaction")

if st.button("Submit"):
    if question:
        answer=f"\"This is a placeholder answer\""
        
        #this will update the consersation in session state
        st.session_state.conversation+=f"You: {question}\nChatPDF: {main(question,file_path)}\n\n"
        
        st.rerun()
        
