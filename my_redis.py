import os
import redis.asyncio as redis
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST=os.getenv("REDIS_HOST")
REDIS_PORT=6379
ACCESS_TOKEN_EXPIRE_SECONDS=os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS")

token_block_list=redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=0
)

async def add_jti_to_blocklist(jti: str)->None:
    await token_block_list.set(
        name=jti,
        value="",
        ex=ACCESS_TOKEN_EXPIRE_SECONDS
    )
    
async def token_in_blocklist(jti: str)->bool:
    jti=await token_block_list.get(jti)
    
    return jti is not None
    

