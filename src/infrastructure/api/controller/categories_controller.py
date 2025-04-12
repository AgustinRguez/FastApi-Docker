from src.application.use_cases.manage_categories import create_category
from src.infrastructure.api.schemas import categories_model
from sqlalchemy.orm import Session
from src.infrastructure.database.connection_orm import get_db
from fastapi import APIRouter, Depends, HTTPException

router_categories = APIRouter(prefix="", tags=[""]) 

@router_categories.post("/create-category")
def create_category_controller(category: categories_model.CreateCategory, db: Session = Depends(get_db)):
    try:
        data = create_category(category=category, db=db)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error posting a category: {str(e)}")