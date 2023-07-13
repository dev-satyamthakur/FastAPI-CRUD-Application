from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

# Creating a model class for create post request
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class PostResponse(Post):
    id: int
    created_at: datetime
    owner_id: int
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

    