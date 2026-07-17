# Seguimiento de flujos (útil para entender decisiones del agente)
from app.core.logging import get_logger
from typing import Any

logger = get_logger("adk.tracer")


class AgentTracer:
    """
    Intercepta eventos del ciclo de vida de Google ADK.
    Captura Chain of Thought, llamadas a Tools y errores intermedios.
    """

    def __init__(self, session_id: str):
        self.session_id = session_id
        self._last_step: str = "Inicializando..."

    @property
    def last_step(self) -> str:
        return self._last_step

    def on_agent_start(self, agent_name: str) -> None:
        self._last_step = f"{agent_name} está iniciando..."
        logger.info(
            "Agente iniciado",
            extra={"session_id": self.session_id, "agent": agent_name, "step": "start"}
        )

    def on_tool_call(self, agent_name: str, tool_name: str, inputs: dict) -> None:
        display_name = {"google_search" : "Google Search",}.get(tool_name, tool_name)  # Mapeo de nombres de herramientas para logs más legibles
        self._last_step = f"{agent_name} está ejecutando: {display_name}"
        logger.info(
            f"Tool invocada: {tool_name}",
            extra={
                "session_id": self.session_id,
                "agent": agent_name,
                "tool": tool_name,
                "step": "tool_call",
            }
        )

    def on_tool_result(self, tool_name: str, success: bool, output_preview: str) -> None:
        status = "exitosa" if success else "fallida"
        self._last_step = f"Tool {tool_name} completada ({status})"
        logger.info(
            f"Tool resultado: {status}",
            extra={
                "session_id": self.session_id,
                "tool": tool_name,
                "step": "tool_result",
                "preview": output_preview[:200],  # no loguear outputs enormes
            }
        )

    def on_thought(self, agent_name: str, thought: str) -> None:
        """Captura el Chain of Thought del LLM cuando ADK lo expone."""
        logger.debug(
            f"Pensamiento del agente",
            extra={
                "session_id": self.session_id,
                "agent": agent_name,
                "step": "thought",
                "thought_preview": thought[:300],
            }
        )

    def on_agent_finish(self, agent_name: str, output_preview: str) -> None:
        self._last_step = f"{agent_name} completó su trabajo"
        logger.info(
            "Agente finalizado",
            extra={
                "session_id": self.session_id,
                "agent": agent_name,
                "step": "finish",
                "output_preview": output_preview[:200],
            }
        )

    def on_error(self, agent_name: str, error: Exception) -> None:
        self._last_step = f"Error en {agent_name}: {type(error).__name__}"
        logger.error(
            f"Error en agente: {error}",
            extra={
                "session_id": self.session_id,
                "agent": agent_name,
                "step": "error",
            },
            exc_info=True
        )