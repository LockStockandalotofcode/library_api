from sqlmodel import SQLModel, Session, select
from database import engine
from models.book import Book
from models.user import User

def seed():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        if session.exec(select(Book)).first():
            print("Already seeded.")
            return
        session.add_all([
            Book(title="Pride and Prejudice", author="Jane Austen"),
            Book(title="Wuthering Heights", author="Emily Brontë"),
            Book(title="War and Peace", author="Leo Tolstoy"),
            User(name="Ben"),
            User(name="Dan"),
        ])
        session.commit()
        print("Seeded.")

if __name__ == "__main__":
    seed()