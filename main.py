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

app = FastAPI(title="Library API", lifespan=lifespan)

app.include_router(books_router)
app.include_router(users_router)
app.include_router(borrowings_router)

@app.get("/")
def home():
    return {"message": "Library API - Visit /docs for all routes."}