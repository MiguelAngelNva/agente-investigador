# Limpieza y formateo de texto (salidas más consistentes)
import re

def clean_llm_output(text: str) -> str:
    """
    Limpia artefactos comunes en outputs de LLMs.
    - Elimina bloques de código markdown innecesarios
    - Normaliza saltos de línea excesivos
    - Elimina caracteres de control
    """
    # Eliminar bloques ```json ... ``` si el contenido no es código
    text = re.sub(r"```(?:json|python|markdown)?\n?(.*?)```", r"\1", text, flags=re.DOTALL)

    # Normalizar saltos de línea: máximo 2 consecutivos
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Eliminar espacios al inicio y final
    text = text.strip()

    return text


def extract_json_from_text(text: str) -> str:
    """
    Extrae el primer bloque JSON válido de un texto mixto.
    Útil cuando el LLM envuelve el JSON en explicaciones.
    """
    # Buscar bloque entre llaves
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)
    return text