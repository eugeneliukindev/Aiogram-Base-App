from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

from aiogram import BaseMiddleware

from src.core.db_manager import db_manager

if TYPE_CHECKING:
    from collections.abc import Awaitable

    from aiogram.types import TelegramObject
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class SessionDepMiddleware(BaseMiddleware):
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession] = db_manager.session_factory,
    ) -> None:
        self.session_factory = session_factory

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        async with self.session_factory() as session:
            data["session"] = session
            return await handler(event, data)
