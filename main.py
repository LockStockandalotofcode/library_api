from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel

from database import engine
from routes.books import router as books_router
from routes.users import router as users_router
from routes.borrowings import router as borrowings_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title="Library Management API",
              description="A RESTful API built with FastAPI, SQLModel, PostgreSQL for managing books, users, and borrowing records.",
              version="1.0.0",
                lifespan=lifespan)

app.include_router(books_router)
app.include_router(users_router)
app.include_router(borrowings_router)

@app.get("/", tags=["Root"])
def home():
    """
    Root endpoint returning a welcome message and quick link to documentation.
    """
    return {"message": "Library API - Visit /docs for interactive documentation."}