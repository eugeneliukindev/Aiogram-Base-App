from __future__ import annotations

from pathlib import Path
from typing import Any, Final
from urllib.parse import quote

from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

from src.utils.enum import LogLevelEnum

BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent

LOG_DEFAULT_FORMAT: Final[str] = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
LOG_DATE_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"


class BotConfig(BaseModel):
    token: str


class BaseDatabaseConfig(BaseModel):
    driver: str = "postgresql+asyncpg"
    host: str = "localhost"
    port: int = 5432
    name: str
    user: str
    password: str

    @property
    def url(self) -> URL:
        return URL.create(
            host=self.host,
            port=self.port,
            database=self.name,
            username=self.user,
            password=self.password,
            drivername=self.driver,
        )

    echo: bool = False
    echo_pool: bool = False

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class DatabaseTestConfig(BaseDatabaseConfig):
    pass


class DatabaseConfig(BaseDatabaseConfig):
    pool_size: int = 50
    max_overflow: int = 10


class RedisConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379
    username: str | None = None
    password: str | None = None
    db: int = 0
    ssl: bool = False

    @property
    def url(self) -> str:
        scheme = "rediss" if self.ssl else "redis"
        auth = ""
        if self.username or self.password:
            username_part = quote(self.username) if self.username else ""
            password_part = quote(self.password) if self.password else ""
            auth = f"{username_part}:{password_part}@"

        return f"{scheme}://{auth}{self.host}:{self.port}/{self.db}"


class LoggingConfig(BaseModel):
    level: LogLevelEnum = LogLevelEnum.DEBUG
    log_format: str = LOG_DEFAULT_FORMAT
    datefmt: str = LOG_DATE_FORMAT

    @field_validator("level", mode="before")
    def validate_log_level(cls, v: Any) -> LogLevelEnum | Any:
        return v.upper() if isinstance(v, str) else v


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            BASE_DIR / ".env-template",
            BASE_DIR / ".env",
        ),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        extra="ignore",
    )

    db: DatabaseConfig
    bot: BotConfig
    redis: RedisConfig = RedisConfig()
    logging: LoggingConfig = LoggingConfig()


settings = Settings()
