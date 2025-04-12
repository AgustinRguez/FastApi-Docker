from src.infrastructure.api.schemas import user_model
from sqlalchemy.orm import Session
from src.infrastructure.utils import hash
from fastapi import HTTPException

def create_user(db: Session, user: user_model.UserCreate):
    try:
        hashed_password = hash(user.password)
        user.password = hashed_password
        new_user = user_model.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error posting a user: {str(e)}")
    
def get_user(db: Session, user_id: int):
    user_found = db.query(user_model.User).filter(user_model.User.id_user == user_id).first()
    if user_found is None:
        raise HTTPException(status_code=500, detail=f"Error getting a user")
    return user_found