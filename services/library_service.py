from datetime import datetime, timedelta
from repositories.book_repo import BookRepository
from repositories.user_repo import UserRepository
from models.book import Book
from models.user import User

class LibraryService:
    def __init__(self):
        self.book_repo = BookRepository()
        self.user_repo = UserRepository()

    # BOOKS
    def get_all_books(self) -> list[Book]:
        return self.book_repo.load_books()

    def get_book_by_id(self, book_id: int) -> Book:
        book = self.book_repo.find_book_by_id(book_id)
        if not book:
            raise ValueError(f"Book {book_id} not found.")
        return book

    def add_book(self, book_data: dict) -> Book:
        books = self.book_repo.load_books()
        new_id = max((book.book_id for book in books), default=0) + 1
        new_book = Book(book_id=new_id, **book_data)
        books.append(new_book)
        self.book_repo.save_books(books)
        return new_book

    def remove_book(self, book_id: int) -> dict:
        books = self.book_repo.load_books()
        book = self.book_repo.find_book_by_id(book_id)
        if not book:
            raise ValueError(f"Book {book_id} not found.")
        books = [b for b in books if b.book_id != book_id]
        self.book_repo.save_books(books)
        return {"message": f"Book {book_id} removed."}

    # USERS
    def get_all_users(self) -> list[User]:
        return self.user_repo.load_users()

    def get_user_by_id(self, user_id: int) -> User:
        user = self.user_repo.find_user_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found.")
        return user

    def get_user_borrowings(self, user_id: int) -> list:
        user = self.get_user_by_id(user_id)
        return user.borrowed_books

    # BORROWINGS
    def borrow_book(self, user_id: int, book_id: int) -> dict:
        # validate request
        user = self.get_user_by_id(user_id)
        book = self.get_book_by_id(book_id)

        # CONSTRAINTS
        if not book.is_available:
            raise ValueError("Book is already borrowed.")
        if len(user.borrowed_books) >= 2:
            raise ValueError(f"Borrowing limit reached for user {user.user_id}.")
        
        # APPLY changes to system
        due_date = (datetime.now() + timedelta(days=7)).strftime("%a %b %d %Y")
        book.is_available = False
        book.due_date = due_date
        user.borrowed_books.append({
            "book_id": book.book_id,
            "title": book.title,
            "due_date": due_date
        })

        # SAVE changes
        books = self.book_repo.load_books()
        users = self.user_repo.load_users()
        # replace with updated user and book
        books = [book if b.book_id == book.book_id else b for b in books]
        users = [user if u.user_id == user.user_id else u for u in users]
        self.book_repo.save_books(books)
        self.user_repo.save_users(users)

        return {"message": "Book borrowed.", "due_date": due_date, "user": user}

    def return_book(self, user_id: int, book_id: int) -> dict:
        # validate request
        user = self.get_user_by_id(user_id)
        book = self.get_book_by_id(book_id)

        # apply changes
        book.is_available = True
        book.due_date = None
        user.borrowed_books = [
            b for b in user.borrowed_books if b.book_id != book_id
        ]

        # SAVE changes
        books = self.book_repo.load_books()
        users = self.user_repo.load_users()
        # replace with updated user and book
        books = [book if b.book_id == book.book_id else b for b in books]
        users = [user if u.user_id == user.user_id else u for u in users]
        self.book_repo.save_books(books)
        self.user_repo.save_users(users)

        return {"message": "Book returned."}
