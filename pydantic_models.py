from pydantic import BaseModel

class Order(BaseModel):
    name: str
    items: int
    
class Chat_history(BaseModel):
    session_id: str
    
