from typing import final

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from app.config import settings
from app.utils.case_converter import camel_case_to_snake_case


class BaseOrm(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(cls.__name__)}s"

    @final
    def __repr__(self) -> str:
        cols = (f"{col.name}={getattr(self, col.name)!r}" for col in self.__table__.columns)
        return f"<{self.__class__.__name__}({', '.join(cols)})>"

    __str__ = __repr__
