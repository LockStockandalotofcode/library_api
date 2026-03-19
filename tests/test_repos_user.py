import pytest
from unittest.mock import patch, mock_open

import json
from repositories.user_repo import UserRepository
from models.user import User

@pytest.fixture
def fake_users_json():
    return json.dumps([
        {"user_id": 1,"name": "Amy","borrowed_books": [] },    {"user_id": 3,"name": "Carey","borrowed_books": []}
    ])

@pytest.fixture
def fake_users_py():
    return [
        User(user_id=1, name="Amy", borrowed_books=[]),
        User(user_id=3, name="Carey", borrowed_books=[]),
    ]

repo = UserRepository()

# LOAD
def test_load_users(fake_users_json):
    with patch("builtins.open", mock_open(read_data=fake_users_json)):
        # act
        users_list = repo.load_users()

        #assert
        assert len(users_list) == 2
        assert isinstance(users_list[0], User)
        assert users_list[1].user_id == 3
        assert users_list[0].name == "Amy"

# SAVE
def test_save_users_correctly_converts_to_json(fake_users_py):
    with patch("builtins.open", mock_open()) as mocked_file, patch("json.dump") as mocked_json_dump:
        # act
        repo.save_users(fake_users_py)

        # assert
        # if called 
        assert mocked_json_dump.called
        # confirm first positional object as data sent by us
        new_users_json_list = mocked_json_dump.call_args[0][0]
        assert len(new_users_json_list) == 2
        assert isinstance(new_users_json_list[0], dict)
        assert new_users_json_list[1]["user_id"] == 3
        assert new_users_json_list[0]["name"] == "Amy"
        assert new_users_json_list[0]["borrowed_books"] == []
        
# # FIND INDIVIDUAL
def test_find_user_by_id(fake_users_json):
    with patch("builtins.open", mock_open(read_data=fake_users_json)):
        # act
        target_user = repo.find_user_by_id(user_id=3)
        
        # assert
        assert target_user is not None
        assert target_user.user_id == 3