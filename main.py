from tkinter.filedialog import askopenfilename
from langchain_community.document_loaders import PyPDFLoader,UnstructuredPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter,CharacterTextSplitter
from vectors import add_to_DB


pdf_path = askopenfilename(filetypes=[("PDF files", "*.pdf")])

def load_documents():
    loader=PyPDFLoader(pdf_path)
    return loader.load()



def split(document):
    splitter_object=CharacterTextSplitter(separator="\n",chunk_size=1000,chunk_overlap=50)
    
    chunks=splitter_object.split_documents(document)
    
    return chunks
   

extracted_documents=load_documents()
# print(extracted_documents)
chunks=split(extracted_documents)
# print(chunks)
# for i,_ in enumerate(chunks):
#     print(f"chunk[{i}]: {chunks[i].page_content} \n")

add_to_DB(chunks)