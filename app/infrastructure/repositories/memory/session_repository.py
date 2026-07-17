from typing import Optional, Dict
from app.domain.research.models import ResearchSession
from app.domain.research.repository_base import ResearchSessionRepository


class InMemorySessionRepository(ResearchSessionRepository):
    """Implementación temporal — Fase 3 la reemplaza por PostgreSQL."""

    def __init__(self):
        self._store: Dict[str, ResearchSession] = {}

    async def save(self, session: ResearchSession) -> None:
        self._store[session.session_id] = session

    async def get(self, session_id: str) -> Optional[ResearchSession]:
        return self._store.get(session_id)


# Instancia única compartida por toda la app
session_repository = InMemorySessionRepository()