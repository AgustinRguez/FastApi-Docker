from fastapi import HTTPException, APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from src.infrastructure.api.schemas import user_model
from src.infrastructure.database.connection_orm import get_db
from src.infrastructure import utils
from src.infrastructure import oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router_auth = APIRouter(tags=['Authentication'], prefix="")

@router_auth.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(user_model.User).filter(user_model.User.email == user_credentials.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    access_token = oauth2.create_access_token(data= {"user_id": user.id_user})
    return {"access_token": access_token, "token_type": "bearer"}
