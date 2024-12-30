from pydantic import BaseModel,Field
  
class Chat_history(BaseModel):
    session_id: str
    
class Query_input(BaseModel):
    file_path:str
    question: str 
    session_id: str = Field(default=None)
    
class Query_output(BaseModel):
    response: str
    session_id: str

    
