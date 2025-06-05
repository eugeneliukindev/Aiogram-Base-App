from sqlalchemy import BigInteger, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import BaseOrm
from app.core.models.mixins import TimestampMixin


class UserOrm(BaseOrm, TimestampMixin):
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str] = mapped_column(String(30))
    username: Mapped[str | None] = mapped_column(String(50), unique=True)
    last_name: Mapped[str | None] = mapped_column(String(30))

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
