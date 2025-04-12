from fastapi import APIRouter, Depends, HTTPException
from src.infrastructure import oauth2
from src.application.use_cases.manage_notes import add_categories_from_notes, create_notes, delete_categories_from_notes, edit_notes, delete_notes, filter_notes_for_categories, get_all_active_notes, get_all_archived_notes
from src.infrastructure.api.schemas import notes_model, access_token_model
from sqlalchemy.orm import Session
from src.infrastructure.database.connection_orm import get_db

router_notes = APIRouter(prefix="", tags=[""]) 

@router_notes.post("/post-notes/{user_id}", response_model= notes_model.NoteResponse)
def create_notes_controller(note_create: notes_model.NoteCreate, user_id: int = Depends(oauth2.get_current_user),
                             db: Session = Depends(get_db)):
    try:
        data = create_notes(note_create,db=db, user_id=user_id)
        return notes_model.NoteResponse(
            id_note=data.id_note,
            archived=data.archived,
            user_id=data.user_id,
            active=data.active,
            category_id=data.category_id
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error posting a note: {str(e)}")
    
@router_notes.put("/edit-notes/{user_id}", response_model= notes_model.NoteEdit)
def edit_notes_controller(note_data: notes_model.NoteEdit, db: Session = Depends(get_db),
                          user_id: access_token_model.TokenData = Depends(oauth2.get_current_user)):
    try:
        data = edit_notes(user_id_param=user_id, note_data=note_data, db=db)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error editing a note: {str(e)}")
    
@router_notes.delete("/delete-notes/{user_id}", response_model= notes_model.NoteDelete)
def delete_notes_controller(note_data: notes_model.NoteDelete, db: Session = Depends(get_db),
                             user_id: int = Depends(oauth2.get_current_user)):
    try:
        data = delete_notes(user_id_param=user_id, note_data=note_data, db=db)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting a note: {str(e)}")
    
@router_notes.get("/get-all-notes-active/{user_id}")
def get_all_active_notes_controller(user_id: int, db: Session = Depends(get_db)):
    try:
        data = get_all_active_notes(user_id_param=user_id, db=db)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting all active notes: {str(e)}")

@router_notes.get("/get-all-notes-archived/{user_id}")
def get_all_archived_notes_controller(user_id: int, db: Session = Depends(get_db)):
    try:
        data = get_all_archived_notes(user_id_param=user_id, db=db)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting all active notes: {str(e)}")
    
@router_notes.delete("/delete-category-note/{user_id_param}")
def delete_categories_from_notes_controller(user_id_param: int, note_data: notes_model.NoteDeleteAddCategory, db: Session=Depends(get_db)):
    try:
        data = delete_categories_from_notes(user_id_param=user_id_param, note_data=note_data, db=db)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting the category from this note: {str(e)}")

@router_notes.post("/add-category-note/{user_id_param}", response_model=notes_model.NoteDeleteAddCategory)
def add_categories_from_notes_controller(user_id_param: int, note_data: notes_model.NoteDeleteAddCategory, db: Session=Depends(get_db)):
    try:
        data = add_categories_from_notes(user_id_param=user_id_param, note_data=note_data, db=db)
        return notes_model.NoteDeleteAddCategory(
            id_note=data.id_note,
            category_id=data.category_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding the category to this note: {str(e)}")

@router_notes.get("/filter-notes-category/{user_id}")
def filter_notes_for_categories_controller(user_id: int, note_data: notes_model.NoteFilterCategory, db: Session = Depends(get_db)):
    try:
        data = filter_notes_for_categories(user_id_param=user_id, note_data=note_data, db=db)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error filtering the category in this user: {str(e)}")