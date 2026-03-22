from fastapi import APIRouter, HTTPException
from services.library_service import LibraryService
from models.book import Book

router = APIRouter(prefix='/books', tags=["Books"])
service = LibraryService()

@router.get("/")
def get_all_books():
    return service.get_all_books()

@router.get("/{book_id}")
def get_book(book_id: int):
    try:
        return service.get_book_by_id(book_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/")
def add_book(book_data: Book):
    try:
        return service.add_book(book_data.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    