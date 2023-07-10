from fastapi import APIRouter, Depends, status, HTTPException, Response
from ..database import get_db
from .. import schemas, models, utils
from sqlalchemy.orm import Session

router = APIRouter(
    tags=['Authentication']
)

@router.post("/login")
async def login(user_cred: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_cred.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    # create a token
    return {"token" : "example"}
