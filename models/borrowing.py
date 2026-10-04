from sqlmodel import SQLModel, Field
from typing import Optional

class Borrowing(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="book.book_id")
    book_id: int = Field(foreign_key="user.user_id")
    due_date: Optional[str] = None