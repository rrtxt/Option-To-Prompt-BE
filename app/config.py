from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database components
    db_username: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str

    @property
    def database_url(self) -> str:
        """Construct database URL from components"""
        return f"postgresql://{self.db_username}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    # API
    api_v1_str: str
    project_name: str

    # CORS
    backend_cors_origins: list[str]

    # Environment
    environment: str
    debug: bool

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
