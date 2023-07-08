from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Creating a model class for create post request
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# Setting up connnection with database
while True:
    try:    
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
                                password='pass', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connected successfully")
        break
    except Exception as e:
        print("Database connection failed - ")
        print("Error : " + str(e))
        time.sleep(2)

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
        
@app.get("/sql")
async def sql(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"status" : posts}

@app.get("/")
async def root():
    return {
            "message" : "Welcome to my API made with FastAPI!!!",
            "name" : "neo"
        }

@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM post""")
    # posts = cursor.fetchall()
    # print(posts)
    posts = db.query(models.Post).all()
    return posts

@app.get("/posts/{id}")
async def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM post WHERE id = %s""", (str(id), ))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    return post

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO post (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
    #                (post.title, post.content, post.published))    
    # db_response = cursor.fetchall()

    # conn.commit()  # commiting to database
    db_response = models.Post(**post.dict())
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return {"data" : db_response}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *""", (str(id), ))
    deleted_post = cursor.fetchone()

    # committing deleted post
    conn.commit()

    print(deleted_post)
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    
    cursor.execute("""UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, str(post.published), str(id), ))

    updated_post = cursor.fetchone()

    # Committing
    conn.commit()
    
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist") 
    return {"message" : "updated successfully", "data" : updated_post}

