from typing import Optional
from sqlmodel import SQLModel, Field

class UserCreate(SQLModel):
    name: str

class User(UserCreate, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)