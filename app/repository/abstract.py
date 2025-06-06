from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

    from pydantic import BaseModel
    from sqlalchemy.ext.asyncio import AsyncSession

    from app.core.models import BaseOrm


class AbstractRepository[ModelT: BaseOrm, CreateST: BaseModel, UpdateST: BaseModel](ABC):
    @classmethod
    @abstractmethod
    async def create(cls, session: AsyncSession, create_schema: CreateST) -> ModelT | None | bool:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def get_by_id(cls, session: AsyncSession, id_: int) -> ModelT | None | bool:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def get_all(cls, session: AsyncSession) -> Sequence[ModelT]:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def update_by_id(cls, session: AsyncSession, id_: int, update_schema: UpdateST) -> ModelT | None | bool:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def delete_by_id(cls, session: AsyncSession, id_: int) -> ModelT | None | bool:
        raise NotImplementedError()
