import streamlit as st

st.title("ChatPDF")
st.header("Your online Ai assistance")

uploaded_file=st.file_uploader("Upload your pdf file here",type="pdf")
