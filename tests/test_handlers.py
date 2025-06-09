from __future__ import annotations

from typing import TYPE_CHECKING, Any
from unittest.mock import AsyncMock, Mock

import aiogram
import pytest
from aiogram.types import Message
from sqlalchemy import insert, select

from app.core.models import UserOrm
from app.handlers.commands import command_start_handler

if TYPE_CHECKING:
    from _pytest.fixtures import SubRequest
    from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
def mock_message(request: SubRequest) -> Mock:
    tg_id, first_name, last_name, username = request.param
    mock_message = Mock(spec=Message)
    aiogram_user = aiogram.types.User(
        id=tg_id,
        first_name=first_name,
        last_name=last_name,
        username=username,
        is_bot=False,
    )
    mock_message.from_user = aiogram_user
    mock_message.reply = AsyncMock()
    return mock_message


class TestCommandStartHandler:
    pytestmark = pytest.mark.parametrize(
        "mock_message",
        [
            (123456789, "Matvey", "Markin", "Matik"),
            (987654321, "Anna", None, None),
            (555555555, "Oleg", None, "oleg_games"),
            (111222333, "Mary", "Blond", None),
        ],
        indirect=True,
    )

    async def test_command_start_handler_new_user(
        self, mock_message: Mock, session: AsyncSession, json_text: Any
    ) -> None:
        await command_start_handler(message=mock_message, session=session)

        mock_message.reply.assert_awaited_once()
        mock_message.reply.assert_awaited_with(json_text["welcome"].format(fullname=mock_message.from_user.full_name))

        stmt = select(UserOrm).filter_by(tg_id=mock_message.from_user.id)
        result = await session.execute(stmt)
        db_user = result.scalars().one()

        assert db_user.tg_id == mock_message.from_user.id
        assert db_user.first_name == mock_message.from_user.first_name
        assert db_user.last_name == mock_message.from_user.last_name
        assert db_user.username == mock_message.from_user.username

    async def test_command_start_handler_existing_user(
        self, mock_message: Mock, session: AsyncSession, json_text: Any
    ) -> None:
        insert(UserOrm).values(
            tg_id=mock_message.from_user.id,
            first_name=mock_message.from_user.first_name,
            last_name=mock_message.from_user.last_name,
            username=mock_message.from_user.username,
        )
        await session.commit()

        stmt = select(UserOrm).filter_by(tg_id=mock_message.from_user.id)
        await session.execute(stmt)
        await command_start_handler(message=mock_message, session=session)
        mock_message.reply.assert_awaited_once()
        mock_message.reply.assert_awaited_with(json_text["already_registered"])
