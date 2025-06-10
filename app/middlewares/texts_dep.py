from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

from aiogram import BaseMiddleware

from app.core.db_manager import db_manager
from app.utils.texts import load_json_text

if TYPE_CHECKING:
    from collections.abc import Awaitable

    from aiogram.types import TelegramObject
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class TextsDepMiddleware(BaseMiddleware):
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
        # You can get the session from `data`, so if you need to send messages in different languages,
        # you can query the database using this session:
        # session: AsyncSession = data["session"]

        texts = await load_json_text()
        data["texts"] = texts
        return await handler(event, data)
