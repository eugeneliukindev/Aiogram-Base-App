from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from datetime import datetime


class UserS(BaseModel):
    id: int
    tg_id: int
    first_name: str
    username: str
    last_name: str

    is_active: bool

    created_at: datetime
    updated_at: datetime


class UserCreateS(BaseModel):
    tg_id: int
    first_name: str
    username: str | None
    last_name: str | None


class UserUpdateS(BaseModel):
    tg_id: int | None = None
    first_name: str | None = None
    username: str | None = None
    last_name: str | None = None
    is_active: bool | None = None
