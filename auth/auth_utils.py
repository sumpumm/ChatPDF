from passlib.context import CryptContext
from .user_database import get_user,create_user
from datetime import datetime,timedelta
from jose import JWTError, jwt
import os,uuid,secrets
from dotenv import load_dotenv
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="token")
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("TOKEN_EXPIRE_MINUTES")
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")


def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)
    
    
def authenticate_user(username: str,password: str):
    user=get_user(username)
    if not user:
        return False
    if not verify_password(password,user['password']):
        return False
    return user


def create_access_token(data: dict):
    to_encode=data.copy()
    expires_delta=timedelta(minutes=15)
    
    expire=datetime.utcnow()+expires_delta
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    return  jwt.encode(data,SECRET_KEY,algorithm=ALGORITHM)


def get_user_token(data: dict, refresh_token=None):
    access_token=create_access_token(data)
    if not refresh_token:
        refresh_token=create_refresh_token(data)
    return access_token,refresh_token


def get_refresh_token(token):
    payload=decode_jwt(token)
    to_encode={"jti":payload["id"],"sub":payload['username'],"session_id":str(secrets.token_hex(16))}
    return get_user_token(to_encode,refresh_token=token) 

def decode_jwt(token):
    payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    return payload


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials")
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception

    except JWTError:
        raise credential_exception
    
    user=get_user(username)
    if not user:
        raise credential_exception
    
    return user

