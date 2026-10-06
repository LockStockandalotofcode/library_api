# Library API

A small REST API for managing a library's books, users, and borrowings — built to learn and demonstrate a clean, layered backend architecture with a real database and a full automated test suite.

## Stack

Python, FastAPI, SQLModel, SQLite, Pytest

## Architecture

Each request flows through four layers, each with one responsibility:

```
routes/        handles HTTP — request in, response or error out
services/      business rules (borrow limits, availability checks)
repositories/  the only layer that talks to the database
models/        SQLModel table definitions (Book, User, Borrowing)
```

Routes never touch the database directly, and repositories know nothing about HTTP — that separation is what makes each layer independently testable.

## Setup

```bash
git clone https://github.com/LockStockandalotofcode/library_api.git
cd library_api
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python seed.py                  # creates library.db with a few starter books and users
uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for interactive API docs, or use the endpoints below directly.

## Endpoints

| Method | Path                    | Description                  |
|--------|--------------------------|-------------------------------|
| GET    | `/books/`                | List all books               |
| GET    | `/books/{book_id}`       | Get one book                 |
| POST   | `/books/`                | Add a book                   |
| DELETE | `/books/{book_id}`       | Remove a book                |
| GET    | `/users/`                | List all users               |
| GET    | `/users/{user_id}`       | Get one user                 |
| POST   | `/users/`                | Add a user                   |
| DELETE | `/users/{user_id}`       | Remove a user                |
| GET    | `/users/{user_id}/borrowings` | List a user's active borrowings |
| POST   | `/borrowings/?user_id=&book_id=` | Borrow a book (7-day due date, 2-book limit per user) |
| DELETE | `/borrowings/?user_id=&book_id=` | Return a book                |

Example:

```bash
curl -X POST "http://127.0.0.1:8000/books/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Clean Code", "author": "Robert C. Martin"}'
```

## Running tests

```bash
pytest -v
```

Every service, repository, and route is covered. Tests run against a temporary in-memory database, so they never touch `library.db`.

## Project structure

```
library_api/
├── main.py
├── database.py
├── seed.py
├── models/        Book, User, Borrowing
├── repositories/  database access only
├── services/      business rules
├── routes/        HTTP endpoints
└── tests/
```

## Possible next steps

Authentication, pagination on list endpoints, and a deployed live demo.