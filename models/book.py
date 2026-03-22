from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    book_id: Optional[int] = None
    title: str
    author: Optional[str] = None
    is_available: Optional[bool] = True
    due_date: Optional[str] = None