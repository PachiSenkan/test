from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    db_url: str = Field(..., alias="DATABASE_URL")

    # model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
