from __future__ import annotations

import inspect
from typing import TYPE_CHECKING

from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_manager import db_manager

if TYPE_CHECKING:
    from collections.abc import Awaitable
    from typing import Any, Callable

    from sqlalchemy.ext.asyncio import async_sessionmaker


class SessionDepMiddleware(BaseMiddleware):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession] = db_manager.session_factory) -> None:
        self.session_factory = session_factory

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        signature = inspect.signature(handler)
        for name, parameter in signature.parameters.items():
            if parameter.annotation is AsyncSession and parameter.default is inspect.Parameter.empty:
                async with self.session_factory() as session:
                    data[name] = session
                    try:
                        return await handler(event, data)
                    except Exception:
                        await session.rollback()
                        raise
                    finally:
                        await session.close()
        return await handler(event, data)
