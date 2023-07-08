from datetime import datetime
from pydantic import BaseModel

# Creating a model class for create post request
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime

    class Config:
        orm_mode = True