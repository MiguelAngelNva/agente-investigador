from app.domain.research.repository_base import MessageRepository
from app.domain.research.models import Message
from app.application.research.services.history_manager import HistoryManager


async def get_session_history(
    session_id: str,
    message_repo: MessageRepository,
) -> list[Message]:
    manager = HistoryManager(message_repo)
    return await manager.get_history(session_id)