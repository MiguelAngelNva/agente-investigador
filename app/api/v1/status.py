from fastapi import APIRouter, HTTPException
from app.schemas.chat_request import StatusResponse
from app.infrastructure.repositories.memory.session_repository import session_repository

router = APIRouter(prefix="/status", tags=["status"])


@router.get("/{session_id}", response_model=StatusResponse)
async def get_status(session_id: str):
    session = await session_repository.get(session_id)

    if session is None:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")

    return StatusResponse(
        session_id=session.session_id,
        status=session.status.value,
        last_step=session.last_step,
        report_markdown=session.report_markdown,
    )