from fastapi import APIRouter, BackgroundTasks, Depends
import uuid
from app.schemas.chat_request import ChatRequest, ChatResponse
from app.application.research.run_investigation import run_investigation
from app.core.dependencies import get_session_repository
from app.domain.research.repository_base import ResearchSessionRepository

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse, status_code=202)
async def chat(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    repo: ResearchSessionRepository = Depends(get_session_repository),
):
    session_id = request.session_id or str(uuid.uuid4())

    background_tasks.add_task(
        run_investigation,
        query=request.query,
        session_id=session_id,
        repo=repo,
    )

    return ChatResponse(
        session_id=session_id,
        status="ACCEPTED",
        message="La investigación ha comenzado. Consulta /status/{session_id} para ver el progreso.",
    )
