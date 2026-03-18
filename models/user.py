from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    user_id: int
    name: str
    borrowed_books: list = []