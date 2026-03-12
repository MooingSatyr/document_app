from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm.attributes import flag_modified

from models.document import Document


class DocumentRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, doc_id: int) -> Document | None:
        return self.db.scalars(
            select(Document).where(Document.id == doc_id)
        ).first()

    def create_doc(self, doc, owner_id: int) -> Document:
        db_doc = Document(
            type=doc.type,
            content=doc.content if isinstance(doc.content, dict) else doc.content.model_dump(),
            owner_id=owner_id
        )

        self.db.add(db_doc)
        self.db.commit()
        self.db.refresh(db_doc)

        return db_doc
    
    def delete_doc(self, doc: Document):

        self.db.delete(doc)
        self.db.commit()


    def get_json_path(self, doc: Document, path: list[str]):
        data = {
            "id": doc.id,
            "type": doc.type,
            "owner_id": doc.owner_id,
            "content": doc.content,
        }

        current = data
        for key in path:
            if not isinstance(current, dict) or key not in current:
                return None
            current = current[key]

        return current
    
    def update_json_path(self, doc: Document, path: list[str], value):
        data = {
            "id": doc.id,
            "type": doc.type,
            "owner_id": doc.owner_id,
            "content": doc.content.copy() if doc.content else {},
        }

        current = data
        for key in path[:-1]:
            if not isinstance(current, dict) or key not in current:
                current[key] = {}
            current = current[key]

        current[path[-1]] = value

        doc.type = data["type"]
        doc.content = data["content"]
        flag_modified(doc, "content")

        self.db.commit()
        self.db.refresh(doc)
        return doc

    def get_all(self) -> list[Document]:
        return self.db.scalars(select(Document)).all()

    def update_content_bulk(self, data: dict, batch_size: int = 100):
        offset = 0
        while True:
            docs = self.db.scalars(
                select(Document).limit(batch_size).offset(offset)
            ).all()
            if not docs:
                break
            for doc in docs:
                content = doc.content.copy()
                content.update(data)
                doc.content = content
                flag_modified(doc, "content")
            self.db.commit()
            offset += batch_size