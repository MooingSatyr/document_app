from unittest.mock import MagicMock
from repositories.document import DocumentRepository



def test_get_by_id():
    db = MagicMock()
    db.scalars.return_value.first.return_value = MagicMock(id=1, content={"key": "value"})

    repo = DocumentRepository(db)
    result = repo.get_by_id(1)

    assert result.id == 1