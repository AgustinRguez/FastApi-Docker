from fastapi import Depends, HTTPException, status
from src.infrastructure.database.connection_orm import get_db
from src.infrastructure.api.schemas import notes_model, user_model, categories_model, access_token_model
from sqlalchemy.orm import Session
from src.infrastructure import oauth2

def create_notes(note_create: notes_model.NoteCreate, db: Session = Depends(get_db), 
                 user_id: access_token_model.TokenData = Depends(oauth2.get_current_user)):
    user = db.query(user_model.User).filter(user_model.User.id_user == user_id.id).first()
    if user is None:
        raise HTTPException(status_code=404, detail=f"Error posting a note, user not exist")
    new_note = notes_model.Notes(
        title = note_create.title,
        content = note_create.content,
        archived = False,
        active = False,
        user_id = user.id_user,
        category_id = note_create.category_id,
        )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

def edit_notes(note_data: notes_model.NoteEdit, db: Session = Depends(get_db),
               user_id_param: access_token_model.TokenData = Depends(oauth2.get_current_user)):
    note = db.query(notes_model.Notes).filter(
        notes_model.Notes.user_id == user_id_param.id, notes_model.Notes.id_note == note_data.id_note)
    note_to_update = note.first()
    if note_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    detail=f"Error updating a note, the note id: {note_data.id_note} with user id: {user_id_param} doesn't exist")
    if note_to_update.user_id != user_id_param.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
    detail=f"Error updating a note, the note id: {note_data.id_note} with user id: {user_id_param} is not authorized")
    note_to_update.title = note_data.title
    note_to_update.content = note_data.content
    note_to_update.archived = note_data.archived
    note_to_update.active = note_data.active
    note_to_update.category_id = note_data.category_id
    db.commit()
    db.refresh(note_to_update)
    return note_to_update #no esta entrando en las validacion de la linea 33, chequear

def delete_notes(note_data: notes_model.NoteDelete, user_id_param: access_token_model.TokenData = Depends(oauth2.get_current_user),
                  db: Session = Depends(get_db)):
    note = db.query(notes_model.Notes).filter(
        notes_model.Notes.user_id == user_id_param.id, notes_model.Notes.id_note == note_data.id_note).first()
    if note is None:
        raise HTTPException(status_code=404, 
    detail=f"Error deleting a note, the note id: {note_data.id_note} with user id: {user_id_param} doesn't exist")
    db.delete(note)
    db.commit()
    return note

def to_dict(instance):
    return {column.name: getattr(instance, column.name) for column in instance.__table__.columns}

def get_all_active_notes(user_id_param: int, db: Session):
    try:
        notes = db.query(notes_model.Notes).filter(
            notes_model.Notes.user_id == user_id_param, notes_model.Notes.active == True
        ).all()
        return [to_dict(i) for i in notes]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting notes: {str(e)}")

def get_all_archived_notes(user_id_param: int, db: Session = Depends(get_db)):
    try:
        notes = db.query(notes_model.Notes).filter(
            notes_model.Notes.user_id == user_id_param, notes_model.Notes.archived == True
        ).all()
        return [to_dict(i) for i in notes]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting notes: {str(e)}")
    
def delete_categories_from_notes(user_id_param: int, note_data: notes_model.NoteDeleteAddCategory, db: Session = Depends(get_db)):
    note = db.query(notes_model.Notes).filter(
        notes_model.Notes.user_id == user_id_param, notes_model.Notes.id_note == note_data.id_note,
        notes_model.Notes.category_id == note_data.category_id
    ).first()
    if note is None:
        raise HTTPException(status_code=404, 
    detail=f"Error deleting a category from note, the note id: {note_data.id_note} with user id: {user_id_param} doesn't exist")
    note.category_id = None
    db.commit()
    return note

def add_categories_from_notes(user_id_param: int, note_data: notes_model.NoteDeleteAddCategory, db: Session = Depends(get_db)):
    note = db.query(notes_model.Notes).filter(
        notes_model.Notes.user_id == user_id_param, notes_model.Notes.id_note == note_data.id_note).first()
    if note is None:
        raise HTTPException(status_code=404, 
    detail=f"Error adding a category to this note, the note id: {note_data.id_note} with user id: {user_id_param} doesn't exist")
    category = db.query(categories_model.Categories).filter(
        categories_model.Categories.id_category == note_data.category_id).first()
    if category is None:
        raise HTTPException(status_code=404,
            detail=f"Error adding a category to note, the note id: {note_data.id_note} with user id: {user_id_param} doesn't exist")
    if note.category_id is not None:
        raise HTTPException(status_code=204, detail=f"Error adding a category, this note already have a category")
    note.category_id = note_data.category_id
    db.commit()
    return note

def filter_notes_for_categories(user_id_param: int, note_data: notes_model.NoteFilterCategory, db: Session=Depends(get_db)):
    note = db.query(notes_model.Notes).filter(
        notes_model.Notes.user_id == user_id_param, notes_model.Notes.category_id == note_data.category_id
    ).all()
    if note is None:
        raise HTTPException(status_code=500, detail=f"Error getting notes")
    if note_data.category_id is None:
        raise HTTPException(status_code=404, detail=f"Error getting notes, user or category doesn't exist")
    return [to_dict(i) for i in note]