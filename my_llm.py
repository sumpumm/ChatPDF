from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings,OllamaLLM
from prompt import llm_prompt
import os,time,uuid
from langchain.docstore.document import Document
from config import get_chat_history,create_logs
from langchain.chains import create_history_aware_retriever,create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain


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


def init_db(file_path):
    embeddings=OllamaEmbeddings(model="nomic-embed-text")

    collection_name=os.path.basename(file_path)

    return Chroma(
        persist_directory="./chroma_langchain_db",
        embedding_function=embeddings,
       collection_name=collection_name 
    ) 

    
def add_docs(file_path,chunks):
    db=init_db(file_path)
    for chunk in chunks:
        chunk_id = str(uuid.uuid4()) 
        page_number = chunk.metadata.get('page')  
        chunk_metadata = {
            "page_number": page_number,
            "source": file_path
        }
        
        document = Document(
            page_content=chunk.page_content,  # The text chunk
            metadata=chunk.metadata,          # The metadata for the chunk
            id=chunk_id                       # The unique ID for the chunk
        )
        # Add chunk to the database with metadata
        db.add_documents([document])
    
    
def doc2str(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def get_rag_chain(file_path,question):
    db=init_db(file_path)
    llm=OllamaLLM(model="llama3")
    
    retriever=db.as_retriever(search_kwargs={"k":2})
    context_text=doc2str(retriever.invoke(question))
    qa_prompt= llm_prompt()
    
    history_aware_retriever=create_history_aware_retriever(llm,retriever,qa_prompt)

    qa_chain=create_stuff_documents_chain(llm,qa_prompt)
    return create_retrieval_chain(history_aware_retriever,qa_chain),context_text
    

def RAG(question,file_path,session_id):
    
    create_logs()
    
    chat_history=get_chat_history(session_id)

    rag_chain,context=get_rag_chain(file_path,question)

    try:
        output=rag_chain.invoke({"chat_history":chat_history,"context":context,"input":question,})
        # print(conversation_chain)
        
        return (output['answer'])
        
    except Exception as e:
        return(f"Error occurred: {e}")