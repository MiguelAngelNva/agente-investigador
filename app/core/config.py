# Variables de entorno (API keys, URLs, settings)
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Google Cloud
    google_cloud_project: str
    google_cloud_location: str = "us-central1"
    google_genai_use_vertexai: bool = True
    google_api_key: str = ""

    # Gemini API
    google_api_key: str
    ia_model: str = "gemini-2.5-flash-lite"
    
    # App
    app_name: str = "Agente Investigador"
    debug: bool = False

    # Base de datos 
    db_backend: str = "firestore" 

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    return Settings()