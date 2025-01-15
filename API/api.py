from fastapi import FastAPI,UploadFile,File,Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic_models import *
import secrets 
from database import get_chat_history,create_logs,insert_log
from my_llm import get_rag_chain,split,add_docs,load_documents
from auth.auth_utils import authenticate_user,create_access_token,get_current_user,get_user,get_password_hash
from auth.user_database import create_user
from datetime import timedelta

# initiliaze the api
app=FastAPI()


@app.post("/register")
async def register_user(username: str,email: str,full_name: str, password: str):
    existing_user_by_username = get_user(username)
    existing_user_by_email = get_user(email)
    if existing_user_by_username or existing_user_by_email:
         raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or Email already exists"
        )
    hashed_password = get_password_hash(password)
    create_user(
        username=username,
        email=email,
        full_name=full_name,
        hashed_password=hashed_password,
    )
    return {"result": True}


@app.post("/token",response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user=authenticate_user(form_data.username,form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect username or password")
    access_token_expires=timedelta(minutes=2)
    access_token=create_access_token(
        data={"sub":user['username']},expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me",response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
 
@app.post("/upload")
async def upload_pdf_endpoint(file: UploadFile=File(...)):
    file_ext=file.filename.split(".").pop()
    if file_ext=="pdf":
        file_name= secrets.token_hex(10)
        file_path=f"uploaded_PDFs/{file_name}.{file_ext}"
        with open(file_path,"wb") as f:
            content= await file.read()
            f.write(content)
        
        chunks=split(load_documents(file_path))
     
        add_docs(file_path,chunks)
        
        return {"success":True, "file_path":file_path, "message":"File uploaded successfully"}
        
    else:
        return {"error":"file must be pdf"}    

@app.get("/chat_history")
async def chat_history_endpoint(session_id: str):
    try:
        messages=get_chat_history(session_id)
        return {"history":messages,"message":"Successful"}        
    except:
        raise Exception("Error connecting to database")
    

@app.post("/chat",response_model=Query_output)
async def chat_endpoint(query_input:Query_input):
    session_id=query_input.session_id
    file_path=query_input.file_path
    question=query_input.question
    temp=query_input.temperature
    top_k=query_input.top_k
    prompt=query_input.prompt
    
    create_logs()
    
    if session_id is None:
        session_id=str(secrets.token_hex(16))
        
    chat_history=get_chat_history(session_id)
    
    rag_chain,context=get_rag_chain(file_path,question,temp,top_k)
    
    try:
        output=rag_chain.invoke({"chat_history":chat_history,"user_prompt":prompt,"context":context,"input":question,})
        response=output['answer']
        insert_log(session_id,question,response,temp,top_k,prompt)
        
        return Query_output(response=response,session_id=session_id)
        
    except Exception as e:
        error_message = f"Error occurred: {str(e)}"
        
        return Query_output(response=error_message, session_id=session_id)