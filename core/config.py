from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    PERIODIC_FETCH_URL: str | None = None
    PERIODIC_FETCH_INTERVAL: int = 30




settings = Settings()