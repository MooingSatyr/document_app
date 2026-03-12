
import httpx
from apscheduler.schedulers.background import BackgroundScheduler

from core.config import settings
from core.database import SessionLocal
from repositories.document import DocumentRepository
from services.document_service import DocumentService


def fetch_and_update_documents():

    url = f"{settings.PERIODIC_FETCH_URL}"

    try:
        response = httpx.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Scheduler fetch error: {e}")
        return

    db = SessionLocal()
    try:
        service = DocumentService(DocumentRepository(db))
        service.merge_external_data(data)
    except Exception as e:
        db.rollback()
        print(f"Scheduler DB error: {e}")
    finally:
        db.close()


def create_scheduler() -> BackgroundScheduler:
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        fetch_and_update_documents,
        trigger="interval",
        seconds=settings.PERIODIC_FETCH_INTERVAL,
    )
    return scheduler