from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BOT_TOKEN: str = "TEST_TOKEN_REPLACE_ME"
    ADMIN_IDS: List[int] = [347382968, 106629087]
    DATABASE_URL: str = "sqlite+aiosqlite:///./besporman.db"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    RATE_LIMIT_BURST: int = 5
    RATE_LIMIT_PERIOD: float = 3.0

    WEBHOOK_MODE: bool = False
    WEBHOOK_URL: str = ""
    WEBHOOK_PATH: str = "/webhook"
    WEBAPP_HOST: str = "0.0.0.0"
    WEBAPP_PORT: int = 8080

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()
