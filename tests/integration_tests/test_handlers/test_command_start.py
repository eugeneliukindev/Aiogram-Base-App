from __future__ import annotations

from typing import TYPE_CHECKING, Any
from unittest.mock import AsyncMock, Mock

import aiogram
import pytest
from aiogram.types import Message
from sqlalchemy import select

from src.core.models import UserOrm
from src.handlers.commands import command_start_handler

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class TestCommandStartHandler:
    @pytest.mark.parametrize(
        "tg_id, first_name, last_name, username, new_user",
        [
            (123456789, "Matvey", "Markin", "Matik", True),
            (987654321, "Anna", None, None, True),
            (555555555, "Oleg", None, "oleg_games", True),
            (111222333, "Mary", "Blond", None, True),
            (444555666, "David", "david_k", "King", False),
            (777888999, "Sophia", "sophia_l", "Lee", False),
            (222333444, "Michael", None, None, False),
        ],
    )
    async def test_command_start_handler(
        self,
        tg_id: int,
        first_name: str,
        last_name: str | None,
        username: str | None,
        new_user: bool,
        session: AsyncSession,
        json_text: Any,
    ) -> None:
        mock_message = Mock(spec=Message)
        user = aiogram.types.User(
            id=tg_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            is_bot=False,
        )
        mock_message.from_user = user
        mock_message.reply = AsyncMock()

        await command_start_handler(message=mock_message, session=session)

        stmt = select(UserOrm).filter_by(tg_id=mock_message.from_user.id)
        result = await session.execute(stmt)

        db_user: UserOrm = result.scalars().one()
        if new_user:
            assert db_user.tg_id == mock_message.from_user.id
            assert db_user.first_name == mock_message.from_user.first_name
            assert db_user.last_name == mock_message.from_user.last_name
            assert db_user.username == mock_message.from_user.username
            mock_message.reply.assert_awaited_with(
                json_text["welcome"].format(fullname=mock_message.from_user.full_name)
            )
        else:
            mock_message.reply.assert_awaited_with(json_text["already_registered"])
        mock_message.reply.assert_awaited_once()
