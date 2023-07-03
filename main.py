from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()

# Creating a model class for create post request
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title" : "Famous places in India", "content" : "Checkout these places in India", "id" : 1}, 
            {"title" : "Best food stalls in Delhi", "content" : "Find delicious food in Delhi", "id" : 2}]

def find_post(id):
    for i in my_posts:
        if i["id"] == id:
            return i
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
async def root():
    return {
            "message" : "Welcome to my API made with FastAPI!!!",
            "name" : "neo"
        }

@app.get("/posts")
async def get_posts():
    return my_posts

@app.get("/posts/{id}")
async def get_post(id: int, response: Response):
    post = find_post(int(id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    return post

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"data" : post_dict}

@app.delete("/posts/{id}")
async def delete_post(id):
    index = find_index_post(int(id))
    my_posts.pop(int(index))
    return {"message" : "post deleted successfully"}

