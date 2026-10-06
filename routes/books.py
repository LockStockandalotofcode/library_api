from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from database import get_session
from services.library_service import LibraryService
from models.book import Book, BookCreate

router = APIRouter(prefix='/books', tags=["Books"])

@router.get("/")
def get_all_books(session: Session = Depends(get_session)):
    return LibraryService(session).get_all_books()

@router.get("/{book_id}")
def get_book(book_id: int, session: Session = Depends(get_session)):
    try:
        return LibraryService(session).get_book_by_id(book_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", response_model=Book, status_code=201)
def add_book(book_data: BookCreate, session = Depends(get_session)):
    try:
        return LibraryService(session).add_book(book_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{book_id}")
def delete_book(book_id: int, session: Session = Depends(get_session)):
    try: 
        return LibraryService(session).remove_book(book_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))