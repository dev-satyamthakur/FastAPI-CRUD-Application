from pydantic import BaseModel

# Creating a model class for create post request
class Post(BaseModel):
    title: str
    content: str
    published: bool = True