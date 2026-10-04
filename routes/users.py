from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from database import get_session
from services.library_service import LibraryService
from models.user import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
def get_all_users(session: Session = Depends(get_session)):
    return LibraryService(session).get_all_users()

@router.get("/{user_id}")
def get_user_by_id(user_id: int, session: Session = Depends(get_session)):
    try:
        return LibraryService(session).get_user_by_id(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/{user_id}/borrowings")
def get_user_borrowings(user_id: int, session: Session = Depends(get_session)):
    try:
        return LibraryService(session).get_user_borrowings(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/")
def add_user(user_data: User, session: Session = Depends(get_session)):
    try:
        return LibraryService(session).add_user(user_data.model_dump(exclude={"user_id"}))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    try: 
        return LibraryService(session).remove_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))