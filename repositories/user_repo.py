import json
from pathlib import Path
from models.user import User

users_file = Path("data/users.json")

class UserRepository:
    def load_users(self) -> list[User]:
        with open(users_file, "r") as f:
            raw_list = json.load(f)
        return [User.model_validate(u) for u in raw_list]
    
    def save_users(self, users: list[User]) -> None:
        with open(users_file, "w") as f:
            json_list = [u.model_dump() for u in users]
            json.dump(json_list, f, indent=2)
    
    def find_user_by_id(self, user_id: int) -> User | None:
        return next((u for u in self.load_users() if u.user_id == user_id), None)