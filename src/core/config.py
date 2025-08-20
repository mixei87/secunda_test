from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_HOST: str = ""
    POSTGRES_PORT: int = 4444
    POSTGRES_DB: str = ""
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    DB_URL_SYNC: str = ""
    DB_URL_ASYNC: str = ""
    API_KEY: str = ""
    DEBUG: bool = False
    ACTIVITY_MAX_DEPTH: int = 3  # Максимальный уровень вложенности активностей

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
