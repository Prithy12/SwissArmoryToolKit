from typing import List, Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "DevOps Toolkit"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]
    
    # File upload settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_EXTENSIONS: List[str] = [".txt", ".yaml", ".yml", ".json", ".diff", ".patch"]
    
    # AI/LLM Settings
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    DEFAULT_AI_PROVIDER: str = "openai"  # "openai" or "anthropic"
    AI_MODEL: str = "gpt-4o-mini"  # or "claude-3-haiku-20240307"
    MAX_TOKENS: int = 4000
    TEMPERATURE: float = 0.1
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./devops_toolkit.db"
    
    # Analysis settings
    MAX_DIFF_SIZE: int = 50000  # Maximum diff size in characters
    ANALYSIS_TIMEOUT: int = 30  # Timeout in seconds
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
