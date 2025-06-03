from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import TYPE_CHECKING

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import BaseOrm

if TYPE_CHECKING:
    pass


class AbstractRepository[M: BaseOrm, CreateS: BaseModel, UpdateS: BaseModel](ABC):
    @classmethod
    @abstractmethod
    async def create(cls, session: AsyncSession, schema: CreateS) -> M | None | bool:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def get_by_id(cls, session: AsyncSession, id_: int) -> M | None:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def get_all(cls, session: AsyncSession) -> Sequence[M]:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def update_by_id(cls, session: AsyncSession, id_: int, schema: UpdateS) -> M | None | bool:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def delete_by_id(cls, session: AsyncSession, id_: int) -> M | None | bool:
        raise NotImplementedError()
