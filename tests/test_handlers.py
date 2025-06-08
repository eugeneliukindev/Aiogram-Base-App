from unittest.mock import AsyncMock, Mock

import aiogram
import pytest
from aiogram.types import Message

from app.handlers.commands import command_start_handler


class TestCommandStartHandler:
    @pytest.mark.parametrize(
        "tg_id, first_name, last_name, username",
        [
            (123456789, "Matvey", "Markin", "Matik"),
            (987654321, "Anna", None, None),
            (555555555, "Oleg", None, "oleg_games"),
            (111222333, "Mary", "Blond", None),
        ],
    )
    async def test_command_start_handler_new_user(self, session, tg_id, first_name, last_name, username):
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
        mock_message.reply.assert_awaited_once()
