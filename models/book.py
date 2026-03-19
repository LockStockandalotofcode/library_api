from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    book_id: int
    title: str
    author: Optional[str]
    is_available: bool = True
    due_date: Optional[str] = None