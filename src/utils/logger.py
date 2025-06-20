from __future__ import annotations

from logging import basicConfig
from typing import TYPE_CHECKING

from src.config import settings

if TYPE_CHECKING:
    from src.utils.enum import LogLevelEnum


def configure_logging(
    level: LogLevelEnum = settings.logging.level,
    format_: str = settings.logging.log_format,
    datefmt: str = settings.logging.datefmt,
) -> None:
    basicConfig(
        level=level,
        format=format_,
        datefmt=datefmt,
    )
