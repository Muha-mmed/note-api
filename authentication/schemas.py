import datetime
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class Create_User(UserBase):
    password: str

class User(BaseModel):
    id: int
    email: EmailStr
    is_active: bool = True
    created_at: datetime.datetime
    update_at : datetime.datetime

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True  # Allow arbitrary types like datetime

class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True  # Allow arbitrary types if needed