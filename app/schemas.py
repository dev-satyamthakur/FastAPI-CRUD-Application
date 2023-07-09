from datetime import datetime
from pydantic import BaseModel, EmailStr

# Creating a model class for create post request
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class PostResponse(Post):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str