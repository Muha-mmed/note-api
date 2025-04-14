from sqlalchemy.orm import Session

from db import engine,Base

from .auth import create_access_token,create_refresh_token,hash_password,verify_password
from .schemas import Create_User
from .models import User

def existing_user(email:str,db:Session):
    return db.query(User).filter(User.email == email).first()

        
    
def create_user_svc(user:Create_User,db: Session):
    check_user = existing_user(user.email,db)
    if check_user:
        return {"message": "user with this email already exist"}
    add_user = User(
        email = user.email,
        password = hash_password(user.password)
    )
    db.add(add_user)
    db.commit()
    return {"message": "user created successfully"}

def loginUser_svc(email:str,password:str,db:Session):
    user = existing_user(email,db)
    if not user or not verify_password(password,user.password):
        return None    
    return {"message": "user login successfully"}

def delete_user_svc(user:User,db:Session):
    current_user = existing_user(user.email,db)
    db.delete(current_user)
    db.commit()
    return {"message": "user deleted"}