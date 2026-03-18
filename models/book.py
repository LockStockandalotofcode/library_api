from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    id: int
    title: str
    author: str
    is_available: bool = True
    due_date: Optional[str] = None