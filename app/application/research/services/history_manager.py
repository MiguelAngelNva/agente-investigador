from app.domain.research.models import Message
from app.domain.research.repository_base import MessageRepository


class HistoryManager:
    def __init__(self, message_repo: MessageRepository):
        self.repo = message_repo

    async def save_turn(
        self, session_id: str, role: str, content: str
    ) -> None:
        message = Message(
            session_id=session_id,
            role=role,
            content=content,
        )
        await self.repo.save_message(message)

    async def get_history(self, session_id: str) -> list[Message]:
        return await self.repo.list_by_session(session_id)

    async def get_history_as_text(self, session_id: str) -> str:
        messages = await self.get_history(session_id)
        if not messages:
            return ""
        lines = [f"[{m.role}]: {m.content}" for m in messages]
        return "\n".join(lines)