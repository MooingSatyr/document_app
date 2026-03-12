from fastapi import HTTPException, status

from repositories.document import DocumentRepository


class DocumentService:

    def __init__(self, repo: DocumentRepository):
        self.repo = repo

    def get_document(self, doc_id: int):
        doc = self.repo.get_by_id(doc_id)

        if not doc:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Document not found")

        return doc

    def get_document_path(self, doc_id: int, path: str):
        doc = self.repo.get_by_id(doc_id)

        if not doc:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Document not found")

        keys = path.split("/")

        return self.repo.get_json_path(doc, keys)

    def update_document_path(self, doc_id: int, path: str, value: dict, user):
        doc = self.repo.get_by_id(doc_id)

        if not doc:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Document not found")

        if doc.owner_id != user.id:
            raise HTTPException(403, "Not allowed")

        keys = path.split("/")

        return self.repo.update_json_path(doc, keys, value)

    def create_document(self, data, user):
        if data.type != user.role:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "You can only create documents matching your role")

        return self.repo.create_doc(data, owner_id=user.id)

    def delete_document(self, doc_id: int, user):
        doc = self.repo.get_by_id(doc_id)

        if not doc:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Document not found")

        if doc.owner_id != user.id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Not allowed")

        self.repo.delete_doc(doc)

        return {"status": "deleted"}

    def compare_documents(self, doc_id1: int, doc_id2: int):
        doc1 = self.repo.get_by_id(doc_id1)
        doc2 = self.repo.get_by_id(doc_id2)

        if not doc1:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Document {doc_id1} not found")
        if not doc2:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Document {doc_id2} not found")

        return self.diff(doc1.content, doc2.content)

    def diff(self, a: dict, b: dict, path: str = ""):
        added: dict = {}
        removed: dict = {}
        changed: dict = {}

        all_keys: set = set(a.keys()) | set(b.keys())

        for key in all_keys:
            full_path: str = f"{path}/{key}" if path else key

            if key not in a:
                added[full_path] = b[key]

            elif key not in b:
                removed[full_path] = a[key]

            elif isinstance(a[key], dict) and isinstance(b[key], dict):
                nested: dict = self.diff(a[key], b[key], full_path)
                added.update(nested["added"])
                removed.update(nested["removed"])
                changed.update(nested["changed"])

            elif a[key] != b[key]:
                changed[full_path] = {"from": a[key], "to": b[key]}

        return {"added": added, "removed": removed, "changed": changed}

    def merge_external_data(self, data: dict):
        self.repo.update_content_bulk(data)