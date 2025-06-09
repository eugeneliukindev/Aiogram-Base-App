from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from sqlalchemy import delete, insert, select, update

from app.core.models import BaseOrm
from app.repository import AbstractRepository

if TYPE_CHECKING:
    from collections.abc import Sequence

    from pydantic import BaseModel
    from sqlalchemy import Result, ScalarResult
    from sqlalchemy.ext.asyncio import AsyncSession


log = logging.getLogger(__name__)


class BaseRepository[ModelT: BaseOrm, CreateST: BaseModel, UpdateST: BaseModel](
    AbstractRepository[ModelT, CreateST, UpdateST]
):
    model_class: type[ModelT]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        if not hasattr(cls, "model_class") or cls.model_class is None:
            msg = "Repository %s must define `model_class`" % cls.__name__
            log.error(msg)
            raise ValueError(msg)
        if not issubclass(cls.model_class, BaseOrm):
            msg = "%s must inherit from BaseOrm" % cls.model_class.__name__
            log.error(msg)
            raise ValueError(msg)

    @classmethod
    async def create(cls, session: AsyncSession, create_schema: CreateST) -> None:
        # fmt: off
        stmt = (
            insert(cls.model_class)
            .values(**create_schema.model_dump())
        )
        # fmt: on
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def _get_by_fields(
        cls, session: AsyncSession, **filter_by: Any
    ) -> ScalarResult[ModelT]:
        # fmt: off
        stmt = (
            select(cls.model_class).
            filter_by(**filter_by)
        )
        # fmt: on
        result: Result[tuple[ModelT, ...]] = await session.execute(stmt)
        scalar_result: ScalarResult[ModelT] = result.scalars()
        return scalar_result

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id_: int) -> ModelT | None:
        scalar_result: ScalarResult[ModelT] = await cls._get_by_fields(
            session=session, id=id_
        )
        model_instance: ModelT | None = scalar_result.one_or_none()
        return model_instance

    @classmethod
    async def get_all(cls, session: AsyncSession) -> Sequence[ModelT]:
        stmt = select(cls.model_class)
        result: Result[tuple[ModelT, ...]] = await session.execute(stmt)
        model_instances: Sequence[ModelT] = result.scalars().all()
        return model_instances

    @classmethod
    async def _update_by_filter_by(
        cls, session: AsyncSession, update_schema: UpdateST, **filter_by: Any
    ) -> None:
        # fmt: off
        stmt = (
            update(cls.model_class)
            .values(**update_schema.model_dump(exclude_unset=True))
            .filter_by(**filter_by)
        )
        # fmt: on
        await session.execute(stmt)

    @classmethod
    async def update_by_id(
        cls, session: AsyncSession, id_: int, update_schema: UpdateST
    ) -> None:
        await cls._update_by_filter_by(
            session=session, update_schema=update_schema, id=id_
        )

    @classmethod
    async def _delete_by_filter_by(
        cls, session: AsyncSession, **filter_by: Any
    ) -> None:
        # fmt: off
        stmt = (
            delete(cls.model_class)
            .filter_by(**filter_by)
        )

        await session.execute(stmt)

    @classmethod
    async def delete_by_id(cls, session: AsyncSession, id_: int) -> None:
        await cls._delete_by_filter_by(session=session, id=id_)
