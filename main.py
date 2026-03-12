# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.v1 import documents, users
from core.scheduler import create_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = create_scheduler()
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(
    title="JSON documents CRUD",
    version="1.0",
    lifespan=lifespan,
)

app.include_router(documents.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "JSON documents CRUD"}

