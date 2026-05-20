# Consulta fuentes web externas.
import httpx
from google.adk.tools import FunctionTool
from app.core.logging import get_logger

logger = get_logger("tools.search_web")


async def _search_web(query: str, max_results: int = 5) -> dict:
    """
    Busca información en la web usando DuckDuckGo (sin API key).
    Devuelve resultados estructurados con título, URL y snippet.

    Args:
        query: Término de búsqueda.
        max_results: Número máximo de resultados a devolver (default 5).

    Returns:
        dict con 'results' (lista de hallazgos) o 'error' si falla.
    """
    logger.info(f"Buscando: {query}")

    try:
        # DuckDuckGo Instant Answer API — sin autenticación
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                "https://api.duckduckgo.com/",
                params={
                    "q": query,
                    "format": "json",
                    "no_redirect": "1",
                    "no_html": "1",
                    "skip_disambig": "1",
                },
            )
            response.raise_for_status()
            data = response.json()

        results = []

        # Respuesta directa (AbstractText)
        if data.get("AbstractText"):
            results.append({
                "title": data.get("Heading", query),
                "url": data.get("AbstractURL", ""),
                "snippet": data["AbstractText"],
                "source": data.get("AbstractSource", ""),
            })

        # Resultados relacionados (RelatedTopics)
        for topic in data.get("RelatedTopics", [])[:max_results]:
            if isinstance(topic, dict) and topic.get("Text"):
                results.append({
                    "title": topic.get("Text", "")[:80],
                    "url": topic.get("FirstURL", ""),
                    "snippet": topic.get("Text", ""),
                    "source": "DuckDuckGo",
                })

        if not results:
            return {
                "results": [],
                "message": f"No se encontraron resultados para: {query}",
            }

        logger.info(f"Encontrados {len(results)} resultados para: {query}")
        return {"results": results[:max_results]}

    except httpx.TimeoutException:
        logger.error(f"Timeout buscando: {query}")
        return {"error": "La búsqueda tardó demasiado. Intenta reformular la consulta."}
    except Exception as e:
        logger.error(f"Error en búsqueda: {e}")
        return {"error": f"Error inesperado: {str(e)}"}


# Empaqueta como FunctionTool para que ADK pueda registrarla
search_web_tool = FunctionTool(_search_web)