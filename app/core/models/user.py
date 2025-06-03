from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import BaseOrm
from app.core.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from sqlalchemy.orm import Mapped


class UserOrm(BaseOrm, TimestampMixin):
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str] = mapped_column(String(30))
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=True)
    last_name: Mapped[str] = mapped_column(String(30), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
