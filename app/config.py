from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    db_url: str = Field(..., alias="DATABASE_URL")


settings = Settings()
