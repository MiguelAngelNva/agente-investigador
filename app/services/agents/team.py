# Orquesta múltiples agentes (flujo ADK)
from google.adk.agents import SequentialAgent
from app.services.agents.investigator import build_investigator
from app.services.agents.editor import build_editor
from app.core.logging import get_logger

logger = get_logger("agents.team")


def build_research_team() -> SequentialAgent:
    """
    Une al Investigador y al Editor en un pipeline secuencial.
    El output del Investigador (investigacion_resultado) se pasa
    automáticamente como contexto al Editor.
    """
    logger.info("Construyendo equipo de investigación...")

    team = SequentialAgent(
        name="equipo_investigacion",
        sub_agents=[
            build_investigator(),
            build_editor(),
        ],
    )

    logger.info("Equipo listo: Investigador → Editor")
    return team