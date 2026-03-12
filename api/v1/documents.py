from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependencies import get_db, get_current_user
from repositories.document import DocumentRepository
from services.document_service import DocumentService

from schemas.documents import DocumentCreate, DocumentRead
from schemas.users import User
from schemas.documents import DocumentDiff

router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)

@router.get("/{doc_id}/{path:path}")
def get_document_path(
    doc_id: int,
    path: str,
    db: Session = Depends(get_db)
):

    service = DocumentService(DocumentRepository(db))

    return service.get_document_path(doc_id, path)

@router.get("/compare", response_model=DocumentDiff)
def compare_documents(
    doc_id1: int,
    doc_id2: int,
    db: Session = Depends(get_db)
):
    service = DocumentService(DocumentRepository(db))
    return service.compare_documents(doc_id1, doc_id2)


@router.get("/{doc_id}", response_model=DocumentRead)
def get_document(
    doc_id: int,
    db: Session = Depends(get_db)
):

    service = DocumentService(DocumentRepository(db))

    return service.get_document(doc_id)


@router.patch("/{doc_id}/{path:path}", response_model=DocumentRead)
def update_document_path(
    doc_id: int,
    path: str,
    value: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    service = DocumentService(DocumentRepository(db))

    return service.update_document_path(
        doc_id,
        path,
        value,
        current_user
    )

@router.post("/", response_model=DocumentRead)
def create_document(
    doc: DocumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    service = DocumentService(DocumentRepository(db))

    return service.create_document(doc, current_user)

@router.delete("/{doc_id}")
def delete_document(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    service = DocumentService(DocumentRepository(db))

    return service.delete_document(doc_id, current_user)