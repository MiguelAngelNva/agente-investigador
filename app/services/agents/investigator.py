import yaml
from pathlib import Path
from google.adk.agents import LlmAgent
from app.services.agents.tools.search.search_web import search_web_tool
from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger("agents.investigator")

_PROMPT_PATH = Path(__file__).parent / "prompts" / "investigator.yaml"


def _load_prompt() -> str:
    with open(_PROMPT_PATH, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    instructions_list = "\n".join(
        f"- {item}" for item in config["instructions"]
    )

    return (
        f"Eres {config['name']}.\n"
        f"Rol: {config['role']}\n\n"
        f"Instrucciones:\n{instructions_list}\n\n"
        f"Formato de salida esperado:\n{config['output_format']}"
    )


def build_investigator() -> LlmAgent:
    logger.info("Construyendo agente Investigador...")

    agent = LlmAgent(
        name="investigador_academico",
        model=get_settings().ia_model,
        instruction=_load_prompt(),
        tools=[search_web_tool],
        output_key="investigacion_resultado",
    )

    logger.info("Agente Investigador listo")
    return agent
