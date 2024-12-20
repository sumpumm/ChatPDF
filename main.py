from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM
from prompt import llm_prompt
import os,time
import uuid
from langchain.docstore.document import Document
from langchain.chains import LLMChain


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

   
def main(question,file_path,memory):
    chunks=split(load_documents(file_path))

    embeddings=OllamaEmbeddings(model="nomic-embed-text")

    collection_name=os.path.basename(file_path)

    db=Chroma(
        persist_directory="./chroma_langchain_db",
        embedding_function=embeddings,
       collection_name=collection_name 
    )  
     
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


    llm=OllamaLLM(model="llama3")
    
    #similarity seach
    results=db.similarity_search_with_score(question,k=2)
    context_text = "\n\n---\n\n".join(doc.page_content for doc, _score in results)
    sources=[doc.metadata for doc,_score in results]

    
    prompt= llm_prompt(context_text)
    
    conversation_chain=LLMChain(
                                llm=llm,
                                prompt=prompt,
                                memory=memory,
                                
                                
    )

    try:
        output=conversation_chain.invoke({"question": question})
        
        return (f"{output["chat_history"][-1].content } \n\n Sources: {sources}")
        
    except Exception as e:
        return(f"Error occurred: {e}")
      


     
      
      
