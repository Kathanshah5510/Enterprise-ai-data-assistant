from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    """Application settings."""

    DATABASE_URL: str | None = os.getenv("DATABASE_URL")
    READONLY_DATABASE_URL: str | None = os.getenv("READONLY_DATABASE_URL")
    SECRET_KEY: str | None = os.getenv("SECRET_KEY")
    ALGORITHM: str | None = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )
    GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
    SQL_TIMEOUT_SECONDS: int = int(os.getenv("SQL_TIMEOUT_SECONDS", "30"))
    SQL_ROW_LIMIT: int = int(os.getenv("SQL_ROW_LIMIT", "500"))
    FAISS_INDEX_PATH: str = os.getenv("FAISS_INDEX_PATH", "embeddings/schema_index")
    CONVERSATION_HISTORY_LIMIT: int = int(os.getenv("CONVERSATION_HISTORY_LIMIT", "10"))


settings = Settings()