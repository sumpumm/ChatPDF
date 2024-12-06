from tkinter.filedialog import askopenfilename
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

pdf_path = askopenfilename(filetypes=[("PDF files", "*.pdf")])

def load_documents():
    loader=PyPDFLoader(pdf_path)
    return loader.load()



def split(documents):
    splitter_object=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50,length_function=len)
    
    chunks=[]
    
    for document in documents:
        chunks.extend(splitter_object.split_text(document.page_content))
    return chunks

extracted_documents=load_documents()
#print(extracted_documents[2:5])
chunks=split(extracted_documents)
for i,_ in enumerate(chunks):
    print(f"chunk[{i}](size: {len(chunks[i])}): {chunks[i]} \n")