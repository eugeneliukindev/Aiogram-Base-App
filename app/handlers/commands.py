from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import Router
from aiogram.filters import CommandStart

from app.core.schemas import UserCreateS
from app.repository.user import UserRepository
from app.utils.texts import load_json_text

if TYPE_CHECKING:
    from aiogram.types import Message
    from sqlalchemy.ext.asyncio import AsyncSession

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, session: AsyncSession) -> None:
    if message.from_user is None:
        return
    json_text = await load_json_text()
    already_registered_message = json_text["already_registered"]
    if await UserRepository.get_by_tg_id(session=session, tg_id=message.from_user.id):
        await message.reply(already_registered_message)
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
    welcome_message: str = json_text["welcome"]
    await message.reply(welcome_message.format(fullname=message.from_user.full_name))
