from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    LOG_FOLDER: str = "logs"

    class Config:
        env_file = ".env"


settings = Settings()
