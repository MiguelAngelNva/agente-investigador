from fastapi import APIRouter, HTTPException, Depends
from app.core.dependencies import get_message_repository
from app.domain.research.repository_base import MessageRepository
from app.application.research.get_history import get_session_history

router = APIRouter(prefix="/history", tags=["history"])


@router.get("/{session_id}", response_model=list[dict])
async def get_history(
    session_id: str,
    message_repo: MessageRepository = Depends(get_message_repository),
):
    messages = await get_session_history(session_id, message_repo)
    if not messages:
        raise HTTPException(
            status_code=404,
            detail="No se encontró historial para esta sesión",
        )
    return [
        {
            "role": m.role,
            "content": m.content,
            "timestamp": m.timestamp.isoformat(),
        }
        for m in messages
    ]