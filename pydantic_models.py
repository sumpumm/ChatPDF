from pydantic import BaseModel,Field
from typing import Optional


class Chat_history(BaseModel):
    session_id: str
    
class Query_input(BaseModel):
    file_path:str
    question: str 
    session_id: str = Field(default=None)
    temperature: float = Field(default=0.8)
    top_k: int = Field(default=2)
    prompt: str 
    
class Query_output(BaseModel):
    response: str
    session_id: str


class Token(BaseModel):
    access_token: str|None=None
    session_id:str
    success: bool =False


class User(BaseModel):
    id: int
    username: str
    email: Optional[str] =None
    full_name: Optional[str] =  None
    

class UserInDB(User):
    hashed_password: str
    

class RegisterUserRequest(BaseModel):
    username: str
    email: str
    full_name: str
    password: str
    

class TokenRevoke(BaseModel):
    token: str