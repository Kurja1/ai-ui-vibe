"""
Configuration loader for the application.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings."""
    
    OLLAMA_HOST: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "gpt-oss:20b"
    
    class Config:
        env_file = ".env"

def get_config() -> Settings:
    """Get configuration instance."""
    return Settings()

# For testing purposes, you can also create a simple config
# that works with localhost