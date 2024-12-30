from fastapi import FastAPI,UploadFile,File
from pydantic_models import *
import secrets 
from config import db_connection,get_chat_history

#initiliaze the api
app=FastAPI()

@app.post("/upload")
async def upload_pdf_endpoint(file: UploadFile=File(...)):
    file_ext=file.filename.split(".").pop()
    if file_ext=="pdf":
        file_name= secrets.token_hex(10)
        file_path=f"uploaded_PDFs/{file_name}.{file_ext}"
        with open(file_path,"wb") as f:
            content= await file.read()
            f.write(content)
        return {"success":True, "file_path":file_path,"message":"File uploaded successfully"}
        
    else:
        return {"error":"file must be pdf"}    

@app.get("/chat_history")
async def chat_history_endpoint(session_id: str):
    try:
        messages=get_chat_history(session_id)
        return {"history":messages,"message":"Successful"}        
    except:
        raise Exception("Error connecting to database")
    
