from typing import List
from sqlalchemy.orm import Session
from app.domain.research.models import Message
from app.domain.research.repository_base import MessageRepository
from app.models.database_models import MessageModel


def _to_domain(model: MessageModel) -> Message:
    return Message(
        session_id=model.session_id,
        role=model.role,
        content=model.content,
        timestamp=model.timestamp,
    )


class PostgresMessageRepository(MessageRepository):

    def __init__(self, db: Session):
        self._db = db

    async def save_message(self, message: Message) -> None:
        model = MessageModel(
            session_id=message.session_id,
            role=message.role,
            content=message.content,
            timestamp=message.timestamp,
        )
        self._db.add(model)
        self._db.commit()

    async def list_by_session(self, session_id: str) -> List[Message]:
        models = (
            self._db.query(MessageModel)
            .filter(MessageModel.session_id == session_id)
            .order_by(MessageModel.timestamp.asc())
            .all()
        )
        return [_to_domain(m) for m in models]