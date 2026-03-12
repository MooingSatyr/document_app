from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from main import app
from core.dependencies import get_db, get_current_user


def test_get_document_not_found():
    mock_db = MagicMock()
    mock_user = MagicMock(id=1, role="commoner")

    app.dependency_overrides[get_db] = lambda: mock_db
    app.dependency_overrides[get_current_user] = lambda: mock_user

    client = TestClient(app)

    with patch("api.v1.documents.DocumentService") as MockService:
        from fastapi import HTTPException
        MockService.return_value.get_document.side_effect = HTTPException(404, "Document not found")
        response = client.get("/documents/999")

    app.dependency_overrides.clear()
    assert response.status_code == 404