from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

import aiofiles

from app.utils.enum import LanguageEnum

if TYPE_CHECKING:
    from typing import Any, Final

ROOT_DIR: Final[Path] = Path(__file__).parent.parent.parent

TEXTS_DIR: Final[Path] = ROOT_DIR / "texts"


async def load_json_text(lang: LanguageEnum = LanguageEnum.EN) -> Any:
    async with aiofiles.open(file=TEXTS_DIR / f"{lang}.json", encoding="utf-8") as f:
        text = await f.read()
        return json.loads(text)
