from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from app.api.v1 import chat, status
from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger("main")
settings = get_settings()

app = FastAPI(title=settings.app_name)

app.include_router(chat.router, prefix="/api/v1")
app.include_router(status.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"status": "ok", "app": settings.app_name}