from sqlmodel import SQLModel, Field
from typing import Optional

class Book(SQLModel, table=True):
    book_id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: Optional[str] = None
    is_available: bool = True
    due_date: Optional[str] = None