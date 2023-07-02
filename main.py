from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

# Creating a model class for create post request
class Post(BaseModel):
    title: str
    content: str

@app.get("/")
async def root():
    return {
            "message" : "Welcome to my API made with FastAPI!!!",
            "name" : "neo"
        }

@app.get("/posts")
async def get_posts():
    return {"data" : "A demo post"}

@app.post("/createposts")
async def create_posts(new_post: Post):
    print(new_post)
    return {"data" : "new_post"}