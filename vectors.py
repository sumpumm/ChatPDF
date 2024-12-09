from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


def embedding_func():
    embeddings=OllamaEmbeddings(model="nomic-embed-text")
    return embeddings

def add_to_DB(chunks):
    db=Chroma(
        persist_directory="./chroma_langchain_db",
        embedding_function=embedding_func()
    )
    db.add_documents(chunks)
    # for chunk in chunks:
        # source=chunk.metadata.get("source")
        # page=chunk.metadata.get("page")
        # id=f"{source}:{page}"
        # db.add_documents(chunk,ids=id)
        # db.persist()