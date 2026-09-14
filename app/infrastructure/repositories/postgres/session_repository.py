from typing import Optional
from sqlalchemy.orm import Session
from app.domain.research.models import ResearchSession
from app.domain.research.repository_base import ResearchSessionRepository
from app.models.database_models import ResearchSessionModel


def _to_domain(model: ResearchSessionModel) -> ResearchSession:
    return ResearchSession(
        session_id=model.session_id,
        status=model.status,
        last_step=model.last_step,
        report_markdown=model.report_markdown,
        created_at=model.created_at,
    )


def _status_value(session: ResearchSession) -> str:
    return session.status.value if hasattr(session.status, "value") else str(session.status)


class PostgresSessionRepository(ResearchSessionRepository):

    def __init__(self, db: Session):
        self._db = db

    async def save(self, session: ResearchSession) -> None:
        existing = (
            self._db.query(ResearchSessionModel)
            .filter(ResearchSessionModel.session_id == session.session_id)
            .one_or_none()
        )
        if existing is None:
            model = ResearchSessionModel(
                session_id=session.session_id,
                status=_status_value(session),
                last_step=session.last_step,
                report_markdown=session.report_markdown,
                created_at=session.created_at,
            )
            self._db.add(model)
        else:
            existing.status = _status_value(session)
            existing.last_step = session.last_step
            existing.report_markdown = session.report_markdown
        self._db.commit()

    async def get(self, session_id: str) -> Optional[ResearchSession]:
        model = (
            self._db.query(ResearchSessionModel)
            .filter(ResearchSessionModel.session_id == session_id)
            .one_or_none()
        )
        if model is None:
            return None
        return _to_domain(model)