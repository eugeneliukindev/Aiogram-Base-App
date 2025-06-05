from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydantic import BaseModel
    from sqlalchemy import ScalarResult
    from sqlalchemy.ext.asyncio import AsyncSession

    from app.core.models import BaseOrm


class AbstractRepository[ModelOrmT: BaseOrm, CreateST: BaseModel, UpdateST: BaseModel](ABC):
    @classmethod
    @abstractmethod
    async def create(cls, session: AsyncSession, create_schema: CreateST) -> ModelOrmT | None | bool:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def get_by_id(cls, session: AsyncSession, id_: int) -> ModelOrmT | None | bool:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def get_all(cls, session: AsyncSession) -> ScalarResult[ModelOrmT] | bool:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def update_by_id(cls, session: AsyncSession, id_: int, update_schema: UpdateST) -> ModelOrmT | None | bool:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def delete_by_id(cls, session: AsyncSession, id_: int) -> ModelOrmT | None | bool:
        raise NotImplementedError()
