from fastapi import APIRouter, HTTPException, Depends
from services.library_service import LibraryService
from database import get_session
from sqlmodel import Session

router = APIRouter(prefix="/borrowings", tags=["Borrowings"])

@router.post("/", summary="Issue a book for a user", description="Issue a book, if not violating borrow limit constraint per user and book is available in the library.")
def borrow_book(user_id: int, book_id: int, session: Session = Depends(get_session)):
    try:
        return LibraryService(session).borrow_book(user_id, book_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/", summary="Return a book from a user", description="Return a book, make it available for future borrowings.")
def return_book(user_id: int, book_id: int, session: Session = Depends(get_session)):
    try:
        return LibraryService(session).return_book(user_id, book_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        