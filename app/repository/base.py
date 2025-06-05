from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from sqlalchemy import delete, select, update

from app.core.models import BaseOrm
from app.repository import AbstractRepository

if TYPE_CHECKING:
    from typing import Any

    from pydantic import BaseModel
    from sqlalchemy import Result, ScalarResult
    from sqlalchemy.ext.asyncio import AsyncSession


log = logging.getLogger(__name__)


class BaseRepository[ModelOrmT: BaseOrm, CreateST: BaseModel, UpdateST: BaseModel](
    AbstractRepository[ModelOrmT, CreateST, UpdateST]
):
    model_class: type[ModelOrmT]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        log.info("Initializing repository subclass: %s", cls.__name__)
        if not hasattr(cls, "model_class") or cls.model_class is None:
            log.error("Invalid model_class in %s: must define a valid model_class", cls.__name__)
            raise ValueError(f"Subclass {cls.__name__} must define a valid model_class")
        log.info("Initialized %s with model: %s", cls.__name__, cls.model_class.__name__)

    @classmethod
    def _validate_field(cls, field: str) -> None:
        log.debug("Validating field '%s' for model %s", field, cls.model_class.__name__)
        if not hasattr(cls.model_class, field):
            log.error("Invalid field '%s' in model %s", field, cls.model_class.__name__)
            raise AttributeError(f"Field '{field}' does not exist in {cls.model_class.__name__}")

    @classmethod
    async def create(cls, session: AsyncSession, create_schema: CreateST) -> ModelOrmT:
        log.info("Creating %s with data: %s", cls.model_class.__name__, create_schema.model_dump())
        instance: ModelOrmT = cls.model_class(**create_schema.model_dump())
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        log.info("Successfully created %s (id=%s)", cls.model_class.__name__, getattr(instance, "id", "unknown"))
        return instance

    @classmethod
    async def _get_by_field(cls, session: AsyncSession, field: str, value: Any) -> ScalarResult[ModelOrmT]:
        log.debug("Querying %s by %s='%s'", cls.model_class.__name__, field, value)
        cls._validate_field(field)
        query = select(cls.model_class).where(getattr(cls.model_class, field) == value)
        result: Result[tuple[ModelOrmT, ...]] = await session.execute(query)
        scalar_result: ScalarResult[ModelOrmT] = result.scalars()
        log.debug("Completed query for %s by %s='%s'", cls.model_class.__name__, field, value)
        return scalar_result

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id_: int) -> ModelOrmT | None:
        log.info("Fetching %s by id=%d", cls.model_class.__name__, id_)
        scalar_result: ScalarResult[ModelOrmT] = await cls._get_by_field(session=session, field="id", value=id_)
        model_orm: ModelOrmT | None = scalar_result.one_or_none()
        log.info(
            "Fetched %s by id=%d: %s",
            cls.model_class.__name__,
            id_,
            "found" if model_orm else "not found",
        )
        return model_orm

    @classmethod
    async def get_all(cls, session: AsyncSession) -> ScalarResult[ModelOrmT]:
        log.info("Fetching all %s records", cls.model_class.__name__)
        query = select(cls.model_class)
        result: Result[tuple[ModelOrmT, ...]] = await session.execute(query)
        scalar_result: ScalarResult[ModelOrmT] = result.scalars()
        log.info("Completed fetching all %s records", cls.model_class.__name__)
        return scalar_result

    @classmethod
    async def _update_by_field(
        cls, session: AsyncSession, field: str, value: Any, update_schema: UpdateST, commit: bool = True
    ) -> ScalarResult[ModelOrmT]:
        log.info(
            "Updating %s by %s='%s' with data: %s",
            cls.model_class.__name__,
            field,
            value,
            update_schema.model_dump(),
        )
        cls._validate_field(field)
        stmt = (
            update(cls.model_class)
            .where(getattr(cls.model_class, field) == value)
            .values(**update_schema.model_dump(exclude_unset=True))
            .returning(cls.model_class)
        )
        result: Result[tuple[ModelOrmT, ...]] = await session.execute(stmt)
        scalar_result: ScalarResult[ModelOrmT] = result.scalars()
        log.info("Completed update for %s by %s='%s'", cls.model_class.__name__, field, value)

        if commit:
            await session.commit()
            log.debug("Committed update for %s by %s='%s'", cls.model_class.__name__, field, value)

        return scalar_result

    @classmethod
    async def update_by_id(cls, session: AsyncSession, id_: int, update_schema: UpdateST) -> ModelOrmT | None:
        log.info("Updating %s by id=%d with data: %s", cls.model_class.__name__, id_, update_schema.model_dump())
        scalar_result: ScalarResult[ModelOrmT] = await cls._update_by_field(
            session=session, field="id", value=id_, update_schema=update_schema
        )
        model_orm: ModelOrmT | None = scalar_result.one_or_none()
        log.info(
            "Updated %s by id=%d: %s",
            cls.model_class.__name__,
            id_,
            "success" if model_orm else "not found",
        )
        return model_orm

    @classmethod
    async def _delete_by_field(
        cls, session: AsyncSession, field: str, value: Any, commit: bool = True
    ) -> ScalarResult[ModelOrmT]:
        log.info("Deleting %s by %s='%s'", cls.model_class.__name__, field, value)
        cls._validate_field(field)
        stmt = delete(cls.model_class).where(getattr(cls.model_class, field) == value).returning(cls.model_class)
        result: Result[tuple[ModelOrmT, ...]] = await session.execute(stmt)
        scalar_result: ScalarResult[ModelOrmT] = result.scalars()
        log.info("Completed deletion for %s by %s='%s'", cls.model_class.__name__, field, value)

        if commit:
            await session.commit()
            log.debug("Committed deletion for %s by %s='%s'", cls.model_class.__name__, field, value)

        return scalar_result

    @classmethod
    async def delete_by_id(cls, session: AsyncSession, id_: int) -> ModelOrmT | None:
        log.info("Deleting %s by id=%d", cls.model_class.__name__, id_)
        scalar_result: ScalarResult[ModelOrmT] = await cls._delete_by_field(session=session, field="id", value=id_)
        model_orm: ModelOrmT | None = scalar_result.one_or_none()
        log.info(
            "Deleted %s by id=%d: %s",
            cls.model_class.__name__,
            id_,
            "success" if model_orm else "not found",
        )
        return model_orm
