import os
from pydantic_settings import BaseSettings
from typing import List
from secrets import token_urlsafe  # For dynamic secret key generation

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Mutual Fund Dashboard"
    
    # Security
    SECRET_KEY: str  # No default - must be set in .env (or generated if missing)
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

# Dynamically generate SECRET_KEY if it's missing
if not settings.SECRET_KEY:
    settings.SECRET_KEY = token_urlsafe(32)  # Generate a random 32-character key

# Print for debugging
print("SECRET_KEY:", settings.SECRET_KEY)
print("DATABASE_URL:", settings.DATABASE_URL)
