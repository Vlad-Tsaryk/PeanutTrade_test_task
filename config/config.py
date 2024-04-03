from typing import Optional, Dict, Any, List

from pydantic import SecretStr, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    SYMBOLS: List[str] = ["btcusdt", "ethusdt", "solusdt"]
    DEVIATION_THRESHOLD: float = 3
    BOT_TOKEN: SecretStr
    CHAT_ID: int

    # POSTGRES_CONF
    POSTGRES_NAME: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_URL: str | None = None

    @validator("POSTGRES_URL", pre=True)
    def validate_postgres_conn(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if isinstance(v, str):
            return v
        password: SecretStr = values.get("POSTGRES_PASSWORD", SecretStr(""))
        return "{scheme}://{user}:{password}@{host}/{db}".format(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=password.get_secret_value(),
            host=values.get("POSTGRES_HOST"),
            db=values.get("POSTGRES_DB"),
        )

    class Config:
        env_file = ".env"


settings = Settings()
