from app.domain.research.models import ResearchSession, ResearchStatus
from app.infrastructure.repositories.memory.session_repository import session_repository
from app.infrastructure.repositories.observability.tracing import AgentTracer
from app.application.research.services.agent_runner import run_team
from app.core.logging import get_logger

logger = get_logger("application.run_investigation")


async def run_investigation(query: str, session_id: str) -> None:
    """
    Flujo completo: crea el registro de sesión, ejecuta el equipo de agentes
    actualizando el estado en tiempo real, y persiste el reporte final.
    """
    tracer = AgentTracer(session_id=session_id)

    session = ResearchSession(
        session_id=session_id,
        status=ResearchStatus.RUNNING,
        last_step="Iniciando investigación...",
    )
    await session_repository.save(session)

    async def on_progress(step: str) -> None:
        session.last_step = step
        await session_repository.save(session)

    try:
        result_markdown = await run_team(
            query=query, session_id=session_id, tracer=tracer, on_progress=on_progress
        )

        session.status = ResearchStatus.COMPLETED
        session.last_step = "Reporte generado correctamente"
        session.report_markdown = result_markdown
        await session_repository.save(session)

        logger.info(f"Investigación completada para session_id={session_id}")

    except Exception as e:
        logger.error(f"Error en investigación: {e}", exc_info=True)
        session.status = ResearchStatus.FAILED
        session.last_step = f"Error: {str(e)}"
        await session_repository.save(session)