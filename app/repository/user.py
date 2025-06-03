from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import delete, select, update

from app.core.models import UserOrm
from app.core.schemas.user import UserCreateS, UserUpdateS
from app.repository import AbstractRepository

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy import Result
    from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(AbstractRepository[UserOrm, UserCreateS, UserUpdateS]):
    @classmethod
    async def create(cls, session: AsyncSession, schema: UserCreateS) -> UserOrm:
        user = UserOrm(**schema.model_dump())
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id_: int) -> UserOrm | None:
        query = select(UserOrm).where(UserOrm.id == id_)
        result: Result[tuple[UserOrm]] = await session.execute(query)
        return result.scalars().one_or_none()

    @classmethod
    async def get_by_tg_id(cls, session: AsyncSession, tg_id: int) -> UserOrm | None:
        query = select(UserOrm).where(UserOrm.tg_id == tg_id)
        result: Result[tuple[UserOrm]] = await session.execute(query)
        return result.scalars().one_or_none()

    @classmethod
    async def get_all(cls, session: AsyncSession) -> Sequence[UserOrm]:
        query = select(UserOrm)
        result: Result[tuple[UserOrm]] = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def update_by_id(cls, session: AsyncSession, id_: int, schema: UserUpdateS) -> UserOrm | None:
        stmt = (
            update(UserOrm).where(UserOrm.id == id_).values(**schema.model_dump(exclude_unset=True)).returning(UserOrm)
        )
        result: Result[tuple[UserOrm]] = await session.execute(stmt)
        return result.scalars().one_or_none()

    @classmethod
    async def update_by_tg_id(cls, session: AsyncSession, tg_id: int, schema: UserUpdateS) -> UserOrm | None:
        stmt = (
            update(UserOrm)
            .where(UserOrm.tg_id == tg_id)
            .values(**schema.model_dump(exclude_unset=True))
            .returning(UserOrm)
        )
        result: Result[tuple[UserOrm]] = await session.execute(stmt)
        return result.scalars().one_or_none()

    @classmethod
    async def delete_by_id(cls, session: AsyncSession, id_: int) -> UserOrm | None:
        stmt = delete(UserOrm).where(UserOrm.id == id_).returning(UserOrm)
        result: Result[tuple[UserOrm]] = await session.execute(stmt)
        return result.scalars().one_or_none()

    @classmethod
    async def delete_by_tg_id(cls, session: AsyncSession, tg_id: int) -> UserOrm | None:
        stmt = delete(UserOrm).where(UserOrm.tg_id == tg_id).returning(UserOrm)
        result: Result[tuple[UserOrm]] = await session.execute(stmt)
        return result.scalars().one_or_none()
