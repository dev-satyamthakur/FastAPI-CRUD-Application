from .. import models, schemas
from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..utils import pwd_context as pass_hasher
from .. import oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# @router.get("/", response_model=List[schemas.PostResponse])
# @router.get("/")
# async def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
#     # cursor.execute("""SELECT * FROM post""")
#     # posts = cursor.fetchall()
#     # print(posts)  

#     posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

#     results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
#         models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    
#     print(posts)
#     return results

@router.get("/")
async def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    query = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).outerjoin(
        models.Vote, models.Vote.post_id == models.Post.id).group_by(models.Post.id)

    if search:
        query = query.filter(models.Post.title.contains(search))

    posts_with_vote_counts = query.limit(limit).offset(skip).all()

    results = []
    for post, vote_count in posts_with_vote_counts:
        post_data = post.__dict__
        post_data["votes"] = vote_count
        results.append(post_data)

    return results

@router.get("/myposts", response_model=List[schemas.PostResponse])
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM post""")
    # posts = cursor.fetchall()
    # print(posts)

    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return posts

@router.get("/{id}", response_model=schemas.PostResponse)
async def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM post WHERE id = %s""", (str(id), ))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")

    # Making user to get only his posts with an id
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Allowed to perform requested action")    

    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_posts(post: schemas.Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO post (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
    #                (post.title, post.content, post.published))    
    # db_response = cursor.fetchall()

    # conn.commit()  # commiting to database

    db_response = models.Post(owner_id=current_user.id, **post.dict())
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *""", (str(id), ))
    # deleted_post = cursor.fetchone()

    # # committing deleted post
    # conn.commit()

    post_to_del = db.query(models.Post).filter(models.Post.id == id)
    post = post_to_del.first()

    if post_to_del.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Allowed to perform requested action")

    
    post_to_del.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.PostResponse)
async def update_post(id: int, post: schemas.Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, str(post.published), str(id), ))

    # updated_post = cursor.fetchone()

    # # Committing
    # conn.commit()

    post_update_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_update_query.first()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist") 
    
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Allowed to perform requested action")
    
    post_update_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_update_query.first()