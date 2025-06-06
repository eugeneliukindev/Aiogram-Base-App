from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from app.core.models import UserOrm
from app.core.schemas import UserCreateS
from app.core.schemas.user import UserUpdateS
from app.repository.base import BaseRepository

if TYPE_CHECKING:
    from sqlalchemy import ScalarResult
    from sqlalchemy.ext.asyncio import AsyncSession

log = logging.getLogger(__name__)


class UserRepository(BaseRepository[UserOrm, UserCreateS, UserUpdateS]):
    model_class: type[UserOrm] = UserOrm

    @classmethod
    async def get_by_tg_id(cls, session: AsyncSession, tg_id: int) -> UserOrm | None:
        scalar_result: ScalarResult[UserOrm] = await cls._get_by_fields(session=session, tg_id=tg_id)
        user: UserOrm | None = scalar_result.one_or_none()
        return user

    @classmethod
    async def update_by_tg_id(cls, session: AsyncSession, tg_id: int, update_schema: UserUpdateS) -> None:
        await cls._update_by_filter_by(
            session=session,
            update_schema=update_schema,
            tg_id=tg_id,
        )

    @classmethod
    async def delete_by_tg_id(cls, session: AsyncSession, tg_id: int) -> None:
        await cls._delete_by_filter_by(session=session, tg_id=tg_id)
