from sqlmodel import SQLModel, Field
from typing import Optional

class BookCreate(SQLModel):
    title: str
    author: Optional[str] = None

class Book(BookCreate, table=True):
    book_id: Optional[int] = Field(default=None, primary_key=True)
    is_available: bool = True
    due_date: Optional[str] = None