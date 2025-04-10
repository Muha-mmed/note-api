from typing import Union
from uuid import UUID
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer,OAuth2PasswordBearer
from jose import JWTError,jwt
from datetime import datetime,timedelta
from decouple import config
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from authentication.models import User
from db import get_db


SECRET_KEY= config('SECRET')
ALGORITHM = config('ALGORITHM')

ACCESS_TOKEN_TIME = 30
REFRESH_TOKEN_TIME = 7

oauth_schema = OAuth2PasswordBearer(tokenUrl="/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_Password:str, hash_password:str)-> bool:
    return pwd_context.verify(plain_Password,hash_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_TIME)
    to_encode.update({"exp": expire})
    encode_jwt= jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_TIME)
    to_encode.update({"exp": expire})
    encode_jwt= jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, token: str) -> bool:
        try:
            jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) 
            return True
        except JWTError:
           return False
       
    def extract_user_id(self, token: str) -> int:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) 
        return payload.get("user_id")


def get_current_user(db: Session = Depends(get_db),token: str = Depends(oauth_schema)):
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Query the database for the user
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        
        return user
    
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )