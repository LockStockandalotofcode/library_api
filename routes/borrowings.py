from fastapi import APIRouter, HTTPException, Depends
from services.library_service import LibraryService
from database import get_session
from sqlmodel import Session

router = APIRouter(prefix="/borrowings", tags=["Borrowings"])

@router.post("/")
def borrow_book(user_id: int, book_id: int, session: Session = Depends(get_session)):
    try:
        return LibraryService(session).borrow_book(user_id, book_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/")
def return_book(user_id: int, book_id: int, session: Session = Depends(get_session)):
    try:
        return LibraryService(session).return_book(user_id, book_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        