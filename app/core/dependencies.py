"""Fábrica central de dependencias de FastAPI.

El repository de sesiones se inyecta en los endpoints y casos de uso
vía Depends(). El singleton de InMemory vive aquí; las implementaciones
Postgres reciben su Session por request.
"""
from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.config import get_settings
from app.core.database import get_db
from app.domain.research.repository_base import (
    ResearchSessionRepository,
    MessageRepository,
)
from app.infrastructure.repositories.memory.session_repository import InMemorySessionRepository
from app.infrastructure.repositories.postgres.session_repository import PostgresSessionRepository
from app.infrastructure.repositories.postgres.message_repository import PostgresMessageRepository

_memory_repository_instance: ResearchSessionRepository | None = None


def _get_memory_repository() -> ResearchSessionRepository:
    global _memory_repository_instance
    if _memory_repository_instance is None:
        _memory_repository_instance = InMemorySessionRepository()
    return _memory_repository_instance


def get_session_repository(
    db: Session = Depends(get_db),
) -> ResearchSessionRepository:
    settings = get_settings()
    if settings.db_backend == "postgres":
        return PostgresSessionRepository(db)
    return _get_memory_repository()


def get_message_repository(
    db: Session = Depends(get_db),
) -> MessageRepository:
    settings = get_settings()
    if settings.db_backend == "postgres":
        return PostgresMessageRepository(db)
    # TODO: Fase 2b — InMemoryMessageRepository si se necesita
    return PostgresMessageRepository(db)