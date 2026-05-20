# Agente que refina / estructura resultados
import yaml
import os
from pathlib import Path
from google.adk.agents import LlmAgent
from app.core.logging import get_logger

logger = get_logger("agents.editor")

_PROMPT_PATH = Path(__file__).parent / "prompts" / "editor.yaml"


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


def build_editor() -> LlmAgent:
    logger.info("Construyendo agente Editor...")

    agent = LlmAgent(
        name="editor_academico",
        model=os.getenv("IA_MODEL"),
        instruction=_load_prompt(),
        tools=[],                          # el Editor solo redacta, no busca
        output_key="reporte_final",
    )

    logger.info("Agente Editor listo")
    return agent