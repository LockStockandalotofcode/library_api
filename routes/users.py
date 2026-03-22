from fastapi import APIRouter, HTTPException
from services.library_service import LibraryService

router = APIRouter(prefix="/users", tags=["Users"])
service = LibraryService()

@router.get("/")
def get_all_users():
    return service.get_all_users()

@router.get("/{user_id}")
def get_user_by_id(user_id: int):
    try:
        return service.get_user_by_id()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/{user_id}/borrowings")
def get_user_borrowings(user_id: int):
    try:
        return service.get_user_borrowings(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
