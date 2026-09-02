"""Fábrica central de dependencias de FastAPI.

El repository de sesiones se inyecta en los endpoints y casos de uso
vía Depends(). El singleton vive aquí, no en el módulo del repository.
"""
from app.core.config import get_settings
from app.domain.research.repository_base import ResearchSessionRepository
from app.infrastructure.repositories.memory.session_repository import InMemorySessionRepository

_repository_instance: ResearchSessionRepository | None = None


def get_session_repository() -> ResearchSessionRepository:
    global _repository_instance
    if _repository_instance is None:
        backend = get_settings().db_backend
        # Fase 2: aquí se añadirá el caso db_backend == "postgres"
        # que devolverá PostgresSessionRepository
        _repository_instance = InMemorySessionRepository()
    return _repository_instance
