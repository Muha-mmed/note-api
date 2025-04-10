from fastapi import APIRouter,Depends, HTTPException

from authentication.auth import JWTBearer, create_access_token, create_refresh_token, get_current_user
from authentication.models import User
from authentication.schemas import Create_User
from authentication.service import create_user_svc,loginUser_svc,existing_user


from sqlalchemy.orm import Session

from db import get_db


auth_route = APIRouter(prefix="/auth",tags=["authentication"])

@auth_route.post("/signup",status_code=201)
def create_user(user:Create_User,db:Session = Depends(get_db)):
    existingUser = existing_user(user.email,db)
    if existingUser:
        raise HTTPException(status_code=403,detail="User already exist")
    create_user_svc(user,db)    
    token = create_access_token({"sub":user.email})
    return {
        "message": "user created successfully",
        "access_token": token
    }
    
@auth_route.post("/login",status_code=200)
def login_user(email: str, password: str,db:Session = Depends(get_db)):
    login_user = loginUser_svc(email, password,db)
    if not login_user:
        raise HTTPException(status_code=409, detail="user not exist")
    token = create_access_token({"sub":email})
    return {
        "message": "user created successfully",
        "access_token": token
    }
    
@auth_route.post("/refresh/token",status_code=201)
def refresh_token(token:str):
    refresh_token = create_refresh_token({"sub":token})
    if not refresh_token:
         return {"message": "invalid access token"}
    return {
        "message": "refresh token created successfully",
        "access_token": refresh_token
    }
    
    
# ✅ Get user info route (No need for JWTBearer, get_current_user already handles it)
@auth_route.get("/user", status_code=200,dependencies=[Depends(JWTBearer())])
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user