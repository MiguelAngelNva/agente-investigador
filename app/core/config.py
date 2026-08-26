from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # Google Cloud
    google_cloud_project: str
    google_cloud_location: str = "us-central1"
    google_genai_use_vertexai: bool = True
    google_api_key: str = ""

    # Gemini API
    ia_model: str = "gemini-2.0-flash"

    # App
    app_name: str = "Agente Investigador"
    debug: bool = False

    # ADK
    adk_app_name: str = "agente-investigador"
    adk_user_id: str = "api-user"

    # Base de datos
    db_backend: str = "firestore"
    database_url: str = ""


@lru_cache()
def get_settings() -> Settings:
    return Settings()
