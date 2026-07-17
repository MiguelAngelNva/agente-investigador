"""
Script de prueba local — ejecutar con:
    python -m scripts.test_team
"""
import asyncio
from dotenv import load_dotenv
load_dotenv()

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from app.services.agents.team import build_research_team
from app.core.logging import get_logger

logger = get_logger("scripts.test_team")

QUERY = "Investiga y redacta un breve resumen la final del mundial de fútbol 2022 entre Argentina y Francia, incluyendo los goles, jugadores destacados y el resultado final."
SESSION_ID = "test-session-001"
APP_NAME = "agente-investigador"


async def main():
    logger.info(f"Iniciando prueba con query: {QUERY}")

    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=APP_NAME,
        user_id="test-user",
        session_id=SESSION_ID,
    )

    team = build_research_team()
    runner = Runner(
        agent=team,
        app_name=APP_NAME,
        session_service=session_service,
    )

    message = Content(parts=[Part(text=QUERY)], role="user")

    print("\n" + "="*60)
    print("INICIANDO AGENTES...")
    print("="*60 + "\n")

    last_agent = None
    final_output = None

    async for event in runner.run_async(
        user_id="test-user",
        session_id=SESSION_ID,
        new_message=message,
    ):
        # Mostrar qué agente está trabajando (sin repetir)
        if event.author and event.author != last_agent:
            print(f"\n▶ [{event.author}] procesando...")
            last_agent = event.author

        # Capturar texto solo cuando hay contenido real
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    final_output = part.text  # siempre guardamos el último

        # Detectar respuesta final del editor específicamente
        if (
            event.is_final_response()
            and event.author == "editor_academico"
            and event.content
            and event.content.parts
        ):
            print("\n" + "="*60)
            print("REPORTE FINAL DEL EDITOR:")
            print("="*60)
            print(event.content.parts[0].text)
            final_output = None  # ya lo imprimimos

    # Si el evento final del SequentialAgent no tiene autor del editor,
    # imprimimos el último texto capturado
    if final_output:
        print("\n" + "="*60)
        print("REPORTE FINAL (último output capturado):")
        print("="*60)
        print(final_output)

    logger.info("Prueba completada")


if __name__ == "__main__":
    asyncio.run(main())