from abc import ABC, abstractmethod
from typing import Optional
from app.domain.research.models import ResearchSession


class ResearchSessionRepository(ABC):

    @abstractmethod
    async def save(self, session: ResearchSession) -> None: ...

    @abstractmethod
    async def get(self, session_id: str) -> Optional[ResearchSession]: ...