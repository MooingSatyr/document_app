# tests/test_user_router.py
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from main import app
from core.dependencies import get_db, get_current_user


def test_create_user_success():
    mock_db = MagicMock()

    app.dependency_overrides[get_db] = lambda: mock_db
    app.dependency_overrides[get_current_user] = lambda: MagicMock(id=1, role="commoner")

    client = TestClient(app)

    with MagicMock() as mock_service:
        from unittest.mock import patch
        with patch("api.v1.users.UserService") as MockService:
            MockService.return_value.create_user.return_value = MagicMock(
                id=1,
                username="timur",
                role="commoner",
                is_active=True
            )
            response = client.post("/users/", json={
                "username": "timur",
                "password": "password123",
                "role": "commoner"
            })

    app.dependency_overrides.clear()
    assert response.status_code == 201