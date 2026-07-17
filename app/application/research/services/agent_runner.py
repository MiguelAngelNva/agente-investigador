from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from app.services.agents.team import build_research_team
from app.infrastructure.repositories.observability.tracing import AgentTracer
from app.core.logging import get_logger

logger = get_logger("application.agent_runner")

APP_NAME = "agente-investigador"
_session_service = InMemorySessionService()


async def run_team(query: str, session_id: str, tracer: AgentTracer, on_progress=None) -> str:

    existing = await _session_service.get_session(
        app_name=APP_NAME, user_id="api-user", session_id=session_id
    )
    if existing is None:
        await _session_service.create_session(
            app_name=APP_NAME, user_id="api-user", session_id=session_id
        )
        logger.info(f"Sesión ADK creada: {session_id}")
    else:
        logger.info(f"Sesión ADK reutilizada: {session_id}")

    team = build_research_team()
    runner = Runner(agent=team, app_name=APP_NAME, session_service=_session_service)
    message = Content(parts=[Part(text=query)], role="user")

    final_output = None
    last_agent = None

    async for event in runner.run_async(
        user_id="api-user", session_id=session_id, new_message=message
    ):
        author = event.author

        if author and author != last_agent:
            tracer.on_agent_start(author)
            last_agent = author
            if on_progress:
                await on_progress(tracer.last_step)

        if event.content and event.content.parts:
            for part in event.content.parts:
                if getattr(part, "function_call", None):
                    tracer.on_tool_call(
                        author,
                        part.function_call.name,
                        dict(part.function_call.args or {}),
                    )
                    if on_progress:
                        await on_progress(tracer.last_step)

                elif getattr(part, "function_response", None):
                    tracer.on_tool_result(
                        part.function_response.name,
                        True,
                        str(part.function_response.response)[:200],
                    )
                    if on_progress:
                        await on_progress(tracer.last_step)

                elif getattr(part, "text", None):
                    final_output = part.text

    tracer.on_agent_finish(last_agent or "equipo", (final_output or "")[:200])
    if on_progress:
        await on_progress(tracer.last_step)

    return final_output or ""