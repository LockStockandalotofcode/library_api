import json
from pathlib import Path
from models.book import Book

books_file = Path("data/books.json")

class BookRepository:
    def load_books(self) -> list[Book]:
        with open(books_file, "r") as f:
            raw_list = json.load(f)
        return [Book.model_validate(b) for b in raw_list]

    def save_books(self, books: list[Book]) -> None:
        with open(books_file, "w") as f:
            json_list = [b.model_dump() for b in books]
            json.dump(json_list, f, indent=2)

    def find_book_by_id(self, book_id: int) -> Book | None:
        return next((b for b in self.load_books() if b.id == book_id), None)