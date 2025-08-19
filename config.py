import os

from pydantic_settings import BaseSettings

current_path = os.path.abspath(__file__)
project_root = os.path.dirname(current_path)


class Settings(BaseSettings):
    # Настройки логгера
    LOG_FOLDER: str = f"{project_root}/logs"
    LOG_LEVEL: str = "INFO"

    # Настройка FastApi
    APP_NAME: str = "RAG Service"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Настройки поиска
    MIN_SIMILARITY_THRESHOLD: float = 0.3
    MAX_SEARCH_RESULTS: int = 10
    VECTOR_DB_PATH: str = f"{project_root}/scripts/vector_db"

    # Настройки чанкера
    DEFAULT_CHUNK_SIZE: int = 512
    DEFAULT_CHUNK_OVERLAP: int = 50

    # GigaChat настройки
    GIGACHAT_API_KEY: str = ""
    GIGACHAT_BASE_URL: str = "https://gigachat.devices.sberbank.ru/api/v1"
    GIGACHAT_MODEL: str = "GigaChat"
    GIGACHAT_SCOPE: str = "GIGACHAT_API_PERS"

    class Config:
        env_file = f"{project_root}/.env"


settings = Settings()
