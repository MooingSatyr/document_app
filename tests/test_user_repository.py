# tests/test_user_repository.py
from unittest.mock import MagicMock
from repositories.user import UserRepository


def test_get_by_username():
    db = MagicMock()
    db.scalars.return_value.first.return_value = MagicMock(username="oleg")

    repo = UserRepository(db)
    result = repo.get_by_username("oleg")

    assert result.username == "oleg"