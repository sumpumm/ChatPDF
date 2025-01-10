from langchain.prompts import ChatPromptTemplate,MessagesPlaceholder,SystemMessagePromptTemplate,HumanMessagePromptTemplate

system_prompt_template = """
    You are an intelligent assistant tasked with finding the most relevant data from a document database. Your name is ChatPDF.
    {user_prompt}.Follow these guidelines during conversations:

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
-**If you've already greeted the user in the conversation history then dont introduce and greet the user again and again.

Based on the given chat history and the latest question of the user which might reference context in the chat history, formulate an answer:

    Context: {context}
    
    Question: {input}

    """

    
def llm_prompt():
    return ChatPromptTemplate.from_messages([
        ("system",system_prompt_template),
        MessagesPlaceholder("chat_history"),
        ("human","{input}"),
        ])

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings,OllamaLLM
import os
from config import get_chat_history
from langchain.chains import create_history_aware_retriever,create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from dotenv import load_dotenv

load_dotenv()
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]=os.getenv("LANGCHAIN_TRACING_V2")



def init_db(file_path):
    embeddings=OllamaEmbeddings(model="nomic-embed-text")

    collection_name=os.path.basename(file_path)

    return Chroma(
        persist_directory="./chroma_langchain_db",
        embedding_function=embeddings,
       collection_name=collection_name 
    ) 

        
def doc2str(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def get_rag_chain(file_path,question,temp,top_k):
    db=init_db(file_path)
    llm=OllamaLLM(model="llama3",temperature=temp)
    
    retriever=db.as_retriever(search_kwargs={"k":top_k})
    context_text=doc2str(retriever.invoke(question))
    qa_prompt= llm_prompt()
    
    history_aware_retriever=create_history_aware_retriever(llm,retriever,qa_prompt)

    qa_chain=create_stuff_documents_chain(llm,qa_prompt)
    return create_retrieval_chain(history_aware_retriever,qa_chain),context_text
    

chat_history=get_chat_history(session_id=None)
question="What is the document about?"
rag_chain,context=get_rag_chain("uploaded_PDFs/39b45b72ae26ca73b3c2.pdf",question,0.8,2)

output=rag_chain.invoke({"chat_history":chat_history,"user_prompt":"Your role is to be friendly.","context":context,"input":question,})

print(output)