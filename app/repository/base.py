from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from sqlalchemy import delete, select, update

from app.core.models import BaseOrm
from app.repository import AbstractRepository

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import Any

    from pydantic import BaseModel
    from sqlalchemy import Result
    from sqlalchemy.ext.asyncio import AsyncSession


log = logging.getLogger(__name__)


class BaseRepository[ModelT: BaseOrm, CreateST: BaseModel, UpdateST: BaseModel](
    AbstractRepository[ModelT, CreateST, UpdateST]
):
    model_class: type[ModelT]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        log.debug("Initializing subclass %s", cls.__name__)
        if not hasattr(cls, "model_class") or cls.model_class is None:
            log.error("Subclass %s must define a valid model_class", cls.__name__)
            raise ValueError(f"Subclass {cls.__name__} must define a valid model_class")
        log.debug("Subclass %s initialized with model_class: %s", cls.__name__, cls.model_class.__name__)

    @classmethod
    def _validate_field(cls, field: str) -> None:
        log.debug("Validating field %s for model %s", field, cls.model_class.__name__)
        if not getattr(cls.model_class, field):
            log.error("Field %s does not exist in %s", field, cls.model_class.__name__)
            raise AttributeError(f"Field {field} does not exist in {cls.model_class.__name__}")

    @classmethod
    async def create(cls, session: AsyncSession, create_schema: CreateST) -> ModelT:
        log.debug("Creating new %s with data: %r", cls.model_class.__name__, create_schema.model_dump())
        instance: ModelT = cls.model_class(**create_schema.model_dump())
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        log.debug("Created %s: %r", cls.model_class.__name__, instance)
        return instance

    @classmethod
    async def _get_by_field(cls, session: AsyncSession, field: str, value: Any) -> Result[tuple[ModelT, ...]]:
        log.debug("Retrieving %s by %s=%r", cls.model_class.__name__, field, value)
        cls._validate_field(field)
        query = select(cls.model_class).where(getattr(cls.model_class, field) == value)
        result: Result[tuple[ModelT, ...]] = await session.execute(query)
        log.debug("Retrieved %s by %s=%r", cls.model_class.__name__, field, value)
        return result

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id_: int) -> ModelT | None:
        log.debug("Fetching %s by id=%d", cls.model_class.__name__, id_)
        result: Result[tuple[ModelT, ...]] = await cls._get_by_field(session=session, field="id", value=id_)
        model: ModelT | None = result.scalars().one_or_none()
        log.debug("Fetched %s by id=%d: %r", cls.model_class.__name__, id_, model)
        return model

    @classmethod
    async def get_all(cls, session: AsyncSession) -> Result[tuple[ModelT, ...]]:
        log.debug("Fetching all %s records", cls.model_class.__name__)
        query = select(cls.model_class)
        result: Result[tuple[ModelT, ...]] = await session.execute(query)
        log.debug("Fetched all %s records", cls.model_class.__name__)
        return result

    @classmethod
    async def get_all_scalars(cls, session: AsyncSession) -> Sequence[ModelT]:
        log.debug("Fetching all %s records as scalars", cls.model_class.__name__)
        result: Result[tuple[ModelT, ...]] = await cls.get_all(session=session)
        scalar_result: Sequence[ModelT] = result.scalars().all()
        log.debug("Fetched %d %s records as scalars", len(scalar_result), cls.model_class.__name__)
        return scalar_result

    @classmethod
    async def _update_by_field(
        cls, session: AsyncSession, field: str, value: Any, update_schema: UpdateST, commit: bool = True
    ) -> Result[tuple[ModelT, ...]]:
        log.debug(
            "Updating %s by %s=%r with data: %r", cls.model_class.__name__, field, value, update_schema.model_dump()
        )
        cls._validate_field(field)
        stmt = (
            update(cls.model_class)
            .where(getattr(cls.model_class, field) == value)
            .values(**update_schema.model_dump(exclude_unset=True))
            .returning(cls.model_class)
        )
        result: Result[tuple[ModelT, ...]] = await session.execute(stmt)
        log.debug("Updated %s by %s=%r", cls.model_class.__name__, field, value)

        if commit:
            await session.commit()
            log.debug("Committed update for %s by %s=%r", cls.model_class.__name__, field, value)

        return result

    @classmethod
    async def update_by_id(cls, session: AsyncSession, id_: int, update_schema: UpdateST) -> ModelT | None:
        log.debug("Updating %s by id=%d with data: %r", cls.model_class.__name__, id_, update_schema.model_dump())
        result: Result[tuple[ModelT, ...]] = await cls._update_by_field(
            session=session, field="id", value=id_, update_schema=update_schema
        )
        model: ModelT | None = result.scalars().one_or_none()
        log.debug("Updated %s by id=%d: %r", cls.model_class.__name__, id_, model)
        return model

    @classmethod
    async def _delete_by_field(
        cls, session: AsyncSession, field: str, value: Any, commit: bool = True
    ) -> Result[tuple[ModelT, ...]]:
        log.debug("Deleting %s by %s=%r", cls.model_class.__name__, field, value)
        cls._validate_field(field)
        stmt = delete(cls.model_class).where(getattr(cls.model_class, field) == value).returning(cls.model_class)
        result: Result[tuple[ModelT, ...]] = await session.execute(stmt)
        log.debug("Deleted %s by %s=%r", cls.model_class.__name__, field, value)

        if commit:
            await session.commit()
            log.debug("Committed deletion for %s by %s=%r", cls.model_class.__name__, field, value)

        return result

    @classmethod
    async def delete_by_id(cls, session: AsyncSession, id_: int) -> ModelT | None:
        log.debug("Deleting %s by id=%d", cls.model_class.__name__, id_)
        result: Result[tuple[ModelT, ...]] = await cls._delete_by_field(session=session, field="id", value=id_)
        model: ModelT | None = result.scalars().one_or_none()
        log.debug("Deleted %s by id=%d: %r", cls.model_class.__name__, id_, model)
        return model
