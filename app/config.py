from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class DatabaseConfig(BaseModel):
    # .env
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

    # .env-template
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env-template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    db: DatabaseConfig


settings = Settings()
