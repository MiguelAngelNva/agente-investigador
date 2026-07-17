from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Pregunta o tema de investigación")
    session_id: Optional[str] = Field(
        default=None, description="UUID de sesión. Si no se envía, se genera uno nuevo."
    )


class ChatResponse(BaseModel):
    session_id: str
    status: str
    message: str


class StatusResponse(BaseModel):
    session_id: str
    status: str
    last_step: str
    report_markdown: Optional[str] = None