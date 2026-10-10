from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from database import get_session
from services.library_service import LibraryService
from models.book import Book, BookCreate

router = APIRouter(prefix='/books', tags=["Books"])

@router.get("/", summary="Retrieve all books", description="Get a list of books currently registered in the Library.")
def get_all_books(session: Session = Depends(get_session)):
    return LibraryService(session).get_all_books()

@router.get("/{book_id}", summary="Retrieve a single book", description="Get a book by its id if registered in the Library.")
def get_book(book_id: int, session: Session = Depends(get_session)):
    try:
        return LibraryService(session).get_book_by_id(book_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", response_model=Book, status_code=201, summary="Add a book", description="Add a book to the Library records.")
def add_book(book_data: BookCreate, session = Depends(get_session)):
    try:
        return LibraryService(session).add_book(book_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{book_id}", summary="Delete a book", description="Delete a book from the Library.")
def delete_book(book_id: int, session: Session = Depends(get_session)):
    try: 
        return LibraryService(session).remove_book(book_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))