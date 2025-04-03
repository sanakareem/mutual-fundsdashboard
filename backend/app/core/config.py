import os
from pydantic.v1 import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Mutual Fund Dashboard"
    
    # Security
    SECRET_KEY: str  # No default - must be set in .env
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database
    DATABASE_URL: str  # Required (no default)
    
    # Connection Pool
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10
    SQL_ECHO: bool = False
    
    # CORS (Critical for Docker)
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",         # Local dev
        "http://frontend:3000",          # Docker service
        "https://your-production-domain.com"  # Production
    ]

    class Config:
        env_file = ".env"
        extra = "forbid"  # Prevent silent failures with typos

settings = Settings()