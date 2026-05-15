from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FinRoute API"
    environment: str = Field(default="local", alias="FINROUTE_ENV")
    api_host: str = Field(default="127.0.0.1", alias="FINROUTE_API_HOST")
    api_port: int = Field(default=8000, alias="FINROUTE_API_PORT")
    cors_origins: str = Field(
        default="http://127.0.0.1:3000,http://localhost:3000",
        alias="FINROUTE_CORS_ORIGINS",
    )
    database_url: str = Field(
        default="postgresql+psycopg://finroute:finroute@localhost:5432/finroute",
        alias="DATABASE_URL",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
