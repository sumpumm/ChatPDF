from tkinter.filedialog import askopenfilename
from langchain_community.document_loaders import PyPDFLoader,UnstructuredPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter,CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaLLM

pdf_path = askopenfilename(filetypes=[("PDF files", "*.pdf")])

def load_documents():
    loader=PyPDFLoader(pdf_path)
    return loader.load()


def split(document):
    splitter_object=CharacterTextSplitter(chunk_size=1000,chunk_overlap=50)
    
    chunks=splitter_object.split_documents(document)
    
    return chunks
   

# extracted_documents=load_documents()
# chunks=split(extracted_documents)

embeddings=OllamaEmbeddings(model="nomic-embed-text")

db=Chroma(
    persist_directory="./chroma_langchain_db",
    embedding_function=embeddings
)
#db.add_documents(chunks)
   

llm=OllamaLLM(model="llama3")
   
qa_chain=RetrievalQA.from_chain_type(
    llm,
    retriever=db.as_retriever()
)

question="the washing is not working"
result=qa_chain.invoke({"query":question})

print(result['result'])