"""Configuration management for the application."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # ZOHO CRM API Configuration
    ZOHO_CLIENT_ID: str
    ZOHO_CLIENT_SECRET: str
    ZOHO_REDIRECT_URI: str
    ZOHO_REFRESH_TOKEN: str
    ZOHO_REGION: str = "US"
    ZOHO_API_DOMAIN: str = "https://www.zohoapis.com"

    # Application Settings
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    DEBUG: bool = False
    MAX_FILE_SIZE_MB: int = 5  # Optimized for T2 Micro (1GB RAM)

    # Lead Configuration
    DEFAULT_LEAD_SOURCE: str = "Document Upload"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
