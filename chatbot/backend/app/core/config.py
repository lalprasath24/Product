import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    
    # API Settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Remo AI - Knowledge Base Chatbot"
    
    # CORS Settings
    ALLOWED_ORIGINS: list = ["*"]

settings = Settings()