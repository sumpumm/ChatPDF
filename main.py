from tkinter.filedialog import askopenfilename
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
import os

pdf_path = askopenfilename(filetypes=[("PDF files", "*.pdf")])

def load_documents():
    loader=PyPDFLoader(pdf_path)
    return loader.load()


def split(document):
    splitter_object=CharacterTextSplitter(chunk_size=1000,chunk_overlap=50)
    
    chunks=splitter_object.split_documents(document)
    
    return chunks
   

extracted_documents=load_documents()
chunks=split(extracted_documents)

embeddings=OllamaEmbeddings(model="nomic-embed-text")

collection_name=os.path.basename(pdf_path)

db=Chroma(
    persist_directory="./chroma_langchain_db",
    embedding_function=embeddings,
    collection_name=collection_name 
)


db.add_documents(chunks)
   

llm=OllamaLLM(model="llama3")
template = """
You are an intelligent assistant tasked with finding the most relevant data from a document database. The database stores PDF content in a vectorized format for efficient search and retrieval. Use the following query to fetch the required information:

Context: {context}

Query: {question}

Answer: 
"""

prompt=PromptTemplate.from_template(template)

   
qa_chain=RetrievalQA.from_chain_type(
    llm=llm,
    retriever=db.as_retriever(),
    chain_type_kwargs={
        "prompt": prompt,
    }
)

while True:
    print("***************MENU***************")
    print("1.Ask a question\n2.Exit")
    
    choice=int(input("Enter your choice: "))
    
    if choice==1:
        question=input("Ask me anything about your document: ")
        try:
            result = qa_chain.invoke({"query": question})
            print(result.get("result", "No result found."))
            print("\n \n \n")
        except Exception as e:
            print(f"Error occurred: {e}")
    elif choice==2:
        print("Goodbye :)")
        break
    else:
        print("Invalid choice")