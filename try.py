import fitz #PyMuPDF
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import uuid
from langchain.docstore.document import Document
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import os


def split(document):
    splitter_object=CharacterTextSplitter()
    
    chunks=splitter_object.split_documents(document)
    
    return chunks

# document=documents.load_page(5)
# print(document.get_text("text"))
# print(documents.metadata)

file_path="manual.pdf"
loader=PyPDFLoader(file_path)
extracted_documents=loader.load()

chunks=split(extracted_documents)
for i in enumerate(chunks):
    print(i)
# embeddings=OllamaEmbeddings(model="nomic-embed-text")

# collection_name=os.path.basename(file_path)

# db=Chroma(
#         persist_directory="./chroma_langchain_db",
#         embedding_function=embeddings,
#        collection_name=collection_name 
#     )  


# for chunk in chunks:
#     chunk_id = str(uuid.uuid4()) 
#     page_number = chunk.metadata.get('page')  
#     chunk_metadata = {
#             "page_number": page_number,
#             "source": file_path
#         }
        
#     document = Document(
#             page_content=chunk.page_content,  # The text chunk
#             metadata=chunk.metadata,          # The metadata for the chunk
#             id=chunk_id                       # The unique ID for the chunk
#         )
#         # Add chunk to the database with metadata
#     db.add_documents([document])

# question="What is the document about?"
#     #similarity seach
# results=db.similarity_search_with_score(question,k=5)

# # for doc,results in results:
# #     print(doc.metadata)

# context_text = "\n\n---\n\n".join(doc.page_content for doc, _score in results)
# print(context_text)