from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings"""
    DATABASE_URL: str = "sqlite:///./finance.db"
    API_TITLE: str = "Personal Finance Tracker"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
