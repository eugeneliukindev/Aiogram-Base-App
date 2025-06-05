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
        scalar_result: ScalarResult[UserOrm] = await cls._get_by_field(session=session, field="tg_id", value=tg_id)
        user_orm: UserOrm | None = scalar_result.one_or_none()
        return user_orm

    @classmethod
    async def update_by_tg_id(cls, session: AsyncSession, tg_id: int, update_schema: UserUpdateS) -> UserOrm | None:
        scalar_result: ScalarResult[UserOrm] = await cls._update_by_field(
            session=session, field="tg_id", value=tg_id, update_schema=update_schema
        )
        updated_user_orm: UserOrm | None = scalar_result.one_or_none()
        return updated_user_orm

    @classmethod
    async def delete_by_tg_id(cls, session: AsyncSession, tg_id: int) -> UserOrm | None:
        scalar_result: ScalarResult[UserOrm] = await cls._delete_by_field(session=session, field="tg_id", value=tg_id)
        deleted_user_orm: UserOrm | None = scalar_result.one_or_none()
        return deleted_user_orm
