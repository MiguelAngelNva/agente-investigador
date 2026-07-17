from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional
from enum import Enum


class ResearchStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ResearchSource(BaseModel):
    url: str
    title: str
    relevance_score: float = Field(ge=0.0, le=1.0)


class ResearchReport(BaseModel):
    """Esquema canónico de un reporte — lo que el sistema DEBE producir."""
    title: str
    summary: str
    findings: list[str]
    bibliography: list[ResearchSource]
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class Message(BaseModel):
    session_id: str
    role: str  # "user" | "investigator" | "editor"
    content: str
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class ResearchSession(BaseModel):
    session_id: str
    status: ResearchStatus = ResearchStatus.PENDING
    last_step: str = "Inicializando..."
    report: Optional[ResearchReport] = None
    report_markdown: Optional[str] = None
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )