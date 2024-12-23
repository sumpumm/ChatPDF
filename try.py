from fastapi import FastAPI
from pydantic_models import *

#initiliaze the api
app=FastAPI()

@app.get("/home")
async def home_endpoint():
    return {"message":"successful"}

@app.get("/greet")
async def greet_endpoint(name: str = 'Samarpan'):
    return {"message":f"hello, {name}"}

@app.post("/order")
async def order_endpoint(name: str ,quantity: int):
    return {"message":f"the order of {quantity} {name} has been placed"}

@app.post("/orderPyd")
async def order_pydantic_endpoint(order: Order):
    return {"message":f"the order of {order.items} {order.name} has been placed"}