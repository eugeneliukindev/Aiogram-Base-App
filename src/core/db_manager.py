from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sqlalchemy import URL, NullPool  # noqa
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import settings

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession


class DatabaseManager:
    def __init__(self, url: str | URL, **engine_kwargs: Any):
        self.engine: AsyncEngine = create_async_engine(url=url, **engine_kwargs)
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )


db_manager = DatabaseManager(
    url=settings.db.url,
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)
