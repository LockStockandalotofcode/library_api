from models.user import User
from sqlmodel import Session, select

class UserRepository:
    def __init__(self, session: Session):
        self.session = Session
    
    def load(self) -> list[User]:
        return self.session.exec(select(User)).all()
    
    def find_user_by_id(self, user_id: int) -> User | None:
        return self.session.get(User, user_id)

    def save(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.session.delete(user)
        self.session.commit()