from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM
from prompt import llm_prompt
import os,time
import uuid
from langchain.docstore.document import Document
from langchain.chains import create_history_aware_retriever,create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from config import db_connection
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_core.messages import HumanMessage,AIMessage
from langchain.prompts import MessagesPlaceholder

file_path="manual.pdf"
template="""
    You are an intelligent assistant tasked with finding the most relevant data from a document database. Your name is ChatPDF.
    You are an advanced AI assistant skilled in both social interactions and providing accurate, up-to-date information. Your role is to be friendly, empathetic, and knowledgeable, adapting your responses to the context and the individual you are speaking with. Follow these guidelines during conversations:

Social Interaction:
- **Tone & Style**: Match the tone of the conversation—professional for formal settings, warm and casual for informal chats, and empathetic for sensitive topics. Maintain politeness and approachability in all interactions.
- **Understanding & Engagement**: Acknowledge the speaker's statements, ask clarifying questions if needed, and respond in a way that feels natural and relevant.
- **Boundaries**: Respect privacy, avoid giving unsolicited opinions, and remain neutral on sensitive topics unless explicitly requested.
- **Conversation Flow**: Offer thoughtful comments, ask engaging questions, and adapt seamlessly between casual talk, storytelling, or idea exchange based on the user’s preferences.

General Knowledge & Information Retrieval:
- **Accuracy**: Provide accurate and concise answers to factual or general knowledge questions, such as "Who is the current president of the United States?" or "What is the capital of France?"
- **Up-to-Date Information**: If the user requests current information, reference the latest knowledge or state limitations when information is unavailable.
- **Clarity**: Ensure your explanations are clear, concise, and easy to understand. If a user asks for additional details, expand on the topic as needed.


Example Scenarios:
- **Social Interaction**: If a user says, "How are you?" in their first message, respond warmly with, "I’m here and ready to help! How about you?" For subsequent queries, engage without repeating a greeting.
- **General Knowledge**: If a user asks, "Who is the current president of the United States?" answer with the correct name and provide context if needed (e.g., "As of December 2024, the President of the United States is Joe Biden.").
- **Blending**: If the user combines both, like "What’s the weather in New York, and what’s a good way to spend the evening there?" answer factually and then offer friendly suggestions.

Strive to make every interaction meaningful, enjoyable, and informative.

Special instructions:
-**If you've already greeted the user in the conversation chain then dont introduce and greet the user again and again.

Based on the given chat history and the latest question of the user which might reference context in the chat history and using the following context formulate an answer:

    
    Question: {input}

    """

contextualized_template="""You are an intelligent assistant tasked with providing accurate and contextually relevant responses. Use the provided chat history and any additional context to answer questions or process requests. If prior messages contain relevant information, incorporate it into your response seamlessly. Ensure clarity and conciseness in your answer.

"""

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
    

def get_chat_history(session_id):
    conn=db_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT message FROM message_store WHERE session_id = %s", (session_id,))


def RAG(question,file_path,chat_history):
    chunks=split(load_documents(file_path))

    db=init_db(file_path)
     
    add_docs(file_path,chunks)

    llm=OllamaLLM(model="llama3")
    
    #similarity seach
    # results=db.similarity_search_with_score(question,k=2)
    # context_text = "\n\n---\n\n".join(doc.page_content for doc, _score in results)
    # sources=[doc.metadata for doc,_score in results]

    retriever=db.as_retriever(search_kwargs={"k":2})
    qa_prompt= llm_prompt()
    
    history_aware_retriever=create_history_aware_retriever(llm,retriever,qa_prompt)

    qa_chain=create_stuff_documents_chain(llm,qa_prompt)
    rag_chain=create_retrieval_chain(history_aware_retriever,qa_chain)

    try:
        output=rag_chain.invoke({"chat_history":chat_history,"input":question,})
        # print(conversation_chain)
        
        return (output['answer'])
        
    except Exception as e:
        return(f"Error occurred: {e}")
      


     
print(RAG("What is the document about?",file_path,chat_history=[]))  

# chunks=split(load_documents(file_path))

# db=init_db(file_path)
     
# add_docs(file_path,chunks)

# llm=OllamaLLM(model="llama3")
    
#     #similarity seach
# retriever=db.as_retriever(search_kwargs={"k":2})

# # print(retriever.invoke("What is the document about?"))

# def doc2str(docs):
#     return "\n\n".join(doc.page_content for doc in docs)

# chat_history=[]

# prompt=ChatPromptTemplate.from_template(template)

# qa_prompt=ChatPromptTemplate.from_messages([
#     ("system",template),
#     ("system","{context}"),
#     MessagesPlaceholder("chat_history"),
#     ("human","{input}"),
# ])

# history_aware_retriever=create_history_aware_retriever(llm,retriever,qa_prompt)

# qa_chain=create_stuff_documents_chain(llm,qa_prompt)
# rag_chain=create_retrieval_chain(history_aware_retriever,qa_chain)

# question="What is the document about?"
# response=rag_chain.invoke({"chat_history":chat_history,"input":question,})
# print(response)

# question="summarize it"
# response=rag_chain.invoke({"chat_history":chat_history,"input":question,})
# print(response)