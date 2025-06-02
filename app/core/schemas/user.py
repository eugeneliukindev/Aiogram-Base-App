from datetime import datetime

from pydantic import BaseModel


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
    username: str
    last_name: str


class UserUpdateS(BaseModel):
    tg_id: int | None = None
    first_name: str | None = None
    username: str | None = None
    last_name: str | None = None
    is_active: bool | None = None
