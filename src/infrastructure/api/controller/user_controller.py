from fastapi import APIRouter, Depends, HTTPException, status
from src.infrastructure.database.connection_orm import get_db
from src.application.use_cases.manage_user import create_user, get_user
from src.infrastructure.api.schemas import user_model
from sqlalchemy.orm import Session

router_user = APIRouter(prefix="", tags=[""]) 

@router_user.post("/post-users", status_code=status.HTTP_201_CREATED)
def create_user_controller(user: user_model.UserCreate, db: Session = Depends(get_db)):
    try:
        data = create_user(db=db, user=user)
        return {"status": "success", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error posting a user: {str(e)}")

@router_user.get("/get-user/{user_id}")
def get_user_controller(user_id: int, db: Session = Depends(get_db)):
    try:
        data = get_user(user_id=user_id, db=db)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Not exist this user: {str(e)}")