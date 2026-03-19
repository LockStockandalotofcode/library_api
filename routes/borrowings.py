from fastapi import APIRouter, HTTPException
from services.library_service import LibraryService

router = APIRouter(prefix="/borrowings", tags=["Borrowings"])
service = LibraryService()

@router.post("/")
def borrow_book(user_id: int, book_id: int):
    try:
        return service.borrow_book(user_id, book_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/")
def return_book(user_id: int, book_id: int):
    try:
        return service.return_book(user_id, book_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        