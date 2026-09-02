from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from app.api.v1 import chat, status
from app.core.config import get_settings
from app.core.logging import get_logger
# get_session_repository se registra automáticamente vía Depends() en los routers

logger = get_logger("main")
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Iniciando con db_backend={settings.db_backend}")
    logger.info(f"Modelo de agentes: {settings.ia_model}")
    yield
    logger.info("Apagando servidor")


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.include_router(chat.router, prefix="/api/v1")
app.include_router(status.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"status": "ok", "app": settings.app_name}
