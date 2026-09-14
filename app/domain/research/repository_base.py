from abc import ABC, abstractmethod
from typing import Optional
from app.domain.research.models import ResearchSession, Message


class ResearchSessionRepository(ABC):

    @abstractmethod
    async def save(self, session: ResearchSession) -> None: ...

    @abstractmethod
    async def get(self, session_id: str) -> Optional[ResearchSession]: ...


class MessageRepository(ABC):

    @abstractmethod
    async def save_message(self, message: Message) -> None: ...

    @abstractmethod
    async def list_by_session(self, session_id: str) -> list[Message]: ...