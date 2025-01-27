from fastapi import FastAPI,UploadFile,File,Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic_models import *
import secrets,uuid
from database import get_chat_history,create_logs,insert_log
from my_llm import get_rag_chain,split,add_docs,load_documents
from auth.auth_utils import authenticate_user,get_user_token,get_current_user,get_user,get_password_hash,decode_jwt,oauth2_scheme
from auth.user_database import create_user,get_user
from datetime import timedelta
from my_redis import add_jti_to_blocklist, token_in_blocklist

# initiliaze the api
app=FastAPI()


@app.post("/register")
async def register_user(request: RegisterUserRequest):
    username = request.username
    email = request.email
    full_name = request.full_name
    password = request.password

    existing_user_by_username = get_user(username)
    existing_user_by_email = get_user(email)
    if existing_user_by_username or existing_user_by_email:
        result=False
        message = "Username/email already in use"
        return {"result": result, "message": message}    
    hashed_password = get_password_hash(password)
    try:
        create_user(
        username=username,
        email=email,
        full_name=full_name,
        password=hashed_password,
        )
        result=True
        message="User registered successfully"
    except Exception as e:
        result=False
        message = f"Error occurred: {str(e)}"
        
    return {"result": result, "message": message}


@app.post("/token",response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user=authenticate_user(form_data.username,form_data.password)
    if not user:
        return {"access_token": None, "success": False}
    user_id=str(get_user(form_data.username)['id'])
    session_id=str(secrets.token_hex(16))
    access_token,refresh_token=get_user_token(data={"jti":user_id,"sub":user['username'],"session_id":session_id}) 
    return {"access_token": access_token,"refresh_token":refresh_token,"session_id":session_id ,"success": True}


@app.get("/refresh_token")
async def refresh_token(token: str):
    payload=decode_jwt(token)
    access_token,refresh_token=get_user_token(payload)
    return {"access_token": access_token,"refresh_token":refresh_token}

@app.get("/users/me",response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.post("/logout")
async def revoke_token(current_token:TokenRevoke):
    payload=decode_jwt(current_token.token)
    jti: str = payload.get("jti")
    if await token_in_blocklist(jti):
        return {"response": "Token already revoked"}
    
    await add_jti_to_blocklist(jti)
    return {"response": "Token revoked successfully, You are logged out"}

    
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
        
        return {"success":True, "file_path":file_path, "response":"File uploaded successfully"}
        
    else:
        return {"error":"file must be pdf"}    

@app.get("/chat_history")
async def chat_history_endpoint(token:Token = Depends(oauth2_scheme)):
    payload=decode_jwt(token.access_token)
    session_id: str=payload.get("session_id")
    try:
        messages=get_chat_history(session_id)
        return {"history":messages,"message":"Successful"}        
    except:
        raise Exception("Error connecting to database")
    

@app.post("/chat",response_model=Query_output)
async def chat_endpoint(query_input:Query_input,current_token: Token = Depends(oauth2_scheme)):
    session_id=query_input.session_id
    file_path=query_input.file_path
    question=query_input.question
    temp=query_input.temperature
    top_k=query_input.top_k
    prompt=query_input.prompt
    try:
        payload=decode_jwt(current_token)
    except Exception as e:
        error_message=f"Error:{str(e)} Please login again"
        return Query_output(response=error_message, session_id=None)
    user=get_user(payload.get("sub"))
    user_id=user["id"]
    create_logs()
  
    chat_history=get_chat_history(session_id)   
    
    rag_chain,context=get_rag_chain(file_path,question,temp,top_k)
    
    try:
        output=rag_chain.invoke({"chat_history":chat_history,"user_prompt":prompt,"context":context,"input":question,})
        response=output['answer']
        insert_log(session_id,user_id,question,response,temp,top_k,prompt)
        
        return Query_output(response=response,session_id=session_id)
        
    except Exception as e:
        error_message = f"Error occurred: {str(e)}"
        
        return Query_output(response=error_message, session_id=session_id)