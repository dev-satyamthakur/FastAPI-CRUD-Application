from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

# Creating a model class for create post request
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title" : "Famous places in India", "content" : "Checkout these places in India", "id" : 1}, 
            {"title" : "Best food stalls in Delhi", "content" : "Find delicious food in Delhi", "id" : 2}]

@app.get("/")
async def root():
    return {
            "message" : "Welcome to my API made with FastAPI!!!",
            "name" : "neo"
        }

@app.get("/posts")
async def get_posts():
    return my_posts

@app.post("/posts")
async def create_posts(post: Post):
    print(post)
    print(post.dict())
    return {"data" : post}