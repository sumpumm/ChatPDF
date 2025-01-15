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
    access_token: str
    token_type: str


class User(BaseModel):
    username: str
    email: Optional[str] =None
    full_name: Optional[str] =  None
    

class UserInDB(User):
    hashed_password: str
    