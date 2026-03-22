from fastapi import FastAPI

from routes.books import router as books_router
from routes.users import router as users_router
from routes.borrowings import router as borrowings_router

app = FastAPI(title="Library API")

app.include_router(books_router)
app.include_router(users_router)
app.include_router(borrowings_router)

@app.get("/")
def home():
    return {"message": "Library API - Visit /docs for all routes."}