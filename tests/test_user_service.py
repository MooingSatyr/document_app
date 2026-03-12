from unittest.mock import MagicMock
import pytest
from fastapi import HTTPException
from services.user_service import UserService


def test_create_user_already_exists():
    repo = MagicMock()
    repo.get_by_username.return_value = MagicMock(username="timur")

    service = UserService(repo)

    with pytest.raises(HTTPException) as exc:
        service.create_user("timur", "password123", "commoner")

    assert exc.value.status_code == 400