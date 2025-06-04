from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from app.core.models import UserOrm
from app.core.schemas import UserCreateS
from app.core.schemas.user import UserUpdateS
from app.repository.base import BaseRepository

if TYPE_CHECKING:
    from sqlalchemy import Result
    from sqlalchemy.ext.asyncio import AsyncSession

log = logging.getLogger(__name__)


class UserRepository(BaseRepository[UserOrm, UserCreateS, UserUpdateS]):
    model_class = UserOrm

    @classmethod
    async def get_by_tg_id(cls, session: AsyncSession, tg_id: int) -> UserOrm | None:
        result: Result[tuple[UserOrm, ...]] = await cls._get_by_field(session=session, field="tg_id", value=tg_id)
        user: UserOrm | None = result.scalars().one_or_none()
        return user

    @classmethod
    async def update_by_tg_id(cls, session: AsyncSession, tg_id: int, schema: UserUpdateS) -> UserOrm | None:
        result: Result[tuple[UserOrm, ...]] = await cls._update_by_field(
            session=session, field="tg_id", value=tg_id, update_schema=schema
        )
        updated_user: UserOrm | None = result.scalars().one_or_none()
        return updated_user

    @classmethod
    async def delete_by_tg_id(cls, session: AsyncSession, tg_id: int) -> UserOrm | None:
        result: Result[tuple[UserOrm, ...]] = await cls._delete_by_field(session=session, field="tg_id", value=tg_id)
        deleted_user: UserOrm | None = result.scalars().one_or_none()
        return deleted_user
