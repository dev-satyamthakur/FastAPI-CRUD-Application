from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from random import randrange
from . import models
from . import schemas
from .database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return {
            "message" : "Welcome to my API made with FastAPI!!!",
            "name" : "neo"
        }

@app.get("/posts", response_model=List[schemas.PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM post""")
    # posts = cursor.fetchall()
    # print(posts)
    posts = db.query(models.Post).all()
    return posts

@app.get("/posts/{id}", response_model=schemas.PostResponse)
async def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM post WHERE id = %s""", (str(id), ))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    return post

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_posts(post: schemas.Post, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO post (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
    #                (post.title, post.content, post.published))    
    # db_response = cursor.fetchall()

    # conn.commit()  # commiting to database
    db_response = models.Post(**post.dict())
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *""", (str(id), ))
    # deleted_post = cursor.fetchone()

    # # committing deleted post
    # conn.commit()

    post_to_del = db.query(models.Post).filter(models.Post.id == id)

    if post_to_del.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    
    post_to_del.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", response_model=schemas.PostResponse)
async def update_post(id: int, post: schemas.Post, db: Session = Depends(get_db)):
    
    # cursor.execute("""UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, str(post.published), str(id), ))

    # updated_post = cursor.fetchone()

    # # Committing
    # conn.commit()

    post_update_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_update_query.first()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist") 
    
    post_update_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_update_query.first()

@app.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):



