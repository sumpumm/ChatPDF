from pydantic import BaseModel

class Order(BaseModel):
    name: str
    items: int
    
