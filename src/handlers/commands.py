from __future__ import annotations

from typing import TYPE_CHECKING, Any

from aiogram import Router
from aiogram.filters import CommandStart

from src.core.schemas import UserCreateS
from src.repository.user import UserRepository

if TYPE_CHECKING:
    from aiogram.types import Message
    from sqlalchemy.ext.asyncio import AsyncSession

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, session: AsyncSession, texts: dict[str, Any]) -> None:
    if message.from_user is None:
        return
    if await UserRepository.get_by_tg_id(session=session, tg_id=message.from_user.id):
        await message.reply(texts["already_registered"])
        return
    create_schema = UserCreateS(
        tg_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )
    await UserRepository.create(
        session=session,
        create_schema=create_schema,
    )
    await message.reply(texts["welcome"].format(fullname=message.from_user.full_name))
