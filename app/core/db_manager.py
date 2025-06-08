from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import NullPool  # noqa
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import settings
from app.utils.enum import ModeEnum

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator
    from typing import Any

    from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession


class DatabaseManager:
    def __init__(self, **engine_kwargs: Any):
        self.engine: AsyncEngine = create_async_engine(**engine_kwargs)
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


db_mapping = {
    ModeEnum.DEV: lambda: DatabaseManager(
        url=settings.db.url,
        echo=settings.db.echo,
        echo_pool=settings.db.echo_pool,
        pool_size=settings.db.pool_size,
        max_overflow=settings.db.max_overflow,
    ),
    ModeEnum.TEST: lambda: DatabaseManager(
        url=settings.db_test.url,
        echo=settings.db_test.echo,
        echo_pool=settings.db_test.echo_pool,
        poolclass=NullPool,  # WARNING! Don't remove this param
    ),
}

db_manager = db_mapping[settings.mode]()  # lazy db getter
