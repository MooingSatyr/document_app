from unittest.mock import MagicMock
import pytest
from fastapi import HTTPException
from services.document_service import DocumentService


def test_delete_document_not_owner():
    repo = MagicMock()
    repo.get_by_id.return_value = MagicMock(id=1, owner_id=1)

    service = DocumentService(repo)
    other_user = MagicMock(id=99)

    with pytest.raises(HTTPException) as exc:
        service.delete_document(1, other_user)

    assert exc.value.status_code == 403