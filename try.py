from my_llm import *
from database import get_chat_history,create_logs

question="What is the document about?"
file_path="test.pdf"
session_id="bcdfb3e92391e90f7418cf832aaa9c19"
chunks=split(load_documents(file_path))
add_docs(file_path,chunks)

def RAG(question,file_path,session_id):
    
    create_logs()
    
    chat_history=get_chat_history(session_id)

    rag_chain,context=get_rag_chain(file_path,question,1,2)
    context_text=context*500
    output=rag_chain.invoke({"chat_history":chat_history,"user_prompt":"you are a PDF ai","context":context_text,"input":question,})
    return output['answer']


print(RAG(question,file_path,session_id))

# db=init_db(file_path)
# chain,context=get_rag_chain(file_path,question,1,2)
# print(context)
# retriever=db.as_retriever(search_kwargs={"k":2})
# context_text=doc2str(retriever.invoke(question))
# print(context_text)