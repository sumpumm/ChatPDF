from langchain_community.document_loaders import PyPDFLoader
#pymupdf
from langchain.text_splitter import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
import os,time


def load_documents(pdf_path):
    loader=PyPDFLoader(pdf_path)
    return loader.load()


def split(document):
    splitter_object=CharacterTextSplitter(chunk_size=1000,chunk_overlap=50)
    
    chunks=splitter_object.split_documents(document)
    
    return chunks

def response_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)
        
   
def main(question,file_path):
    chunks=split(load_documents(file_path))

    embeddings=OllamaEmbeddings(model="nomic-embed-text")

    collection_name=os.path.basename(file_path)

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

    # question=input("Ask me anything about your document: ")
    try:
        result = qa_chain.invoke({"query": question,
                                          "context": "context"})
        return(result.get("result", "No result found."))
        
    except Exception as e:
        return(f"Error occurred: {e}")
      