from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any

import pytest
import pytest_asyncio
from _pytest.config import UsageError
from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio.connection import parse_url as parse_redis_url
from redis.exceptions import ConnectionError
from sqlalchemy import NullPool, insert

from src.config import settings
from src.core.db_manager import DatabaseManager
from src.core.models import BaseOrm, UserOrm
from src.utils.texts import load_json_text
from tests.integration_tests.utils import MOCK_USERS
from tests.mock_bot import MockedBot

if TYPE_CHECKING:
    from asyncio import AbstractEventLoop
    from collections.abc import AsyncGenerator, Generator

    from _pytest.fixtures import SubRequest
    from sqlalchemy.ext.asyncio import AsyncSession

SKIP_MESSAGE_PATTERN = 'Need "--{db}" option with {db} URI to run'
INVALID_URI_PATTERN = "Invalid {db} URI {uri!r}: {err}"

db_test_manager = DatabaseManager(
    url=settings.db_test.url,
    echo=settings.db_test.echo,
    echo_pool=settings.db_test.echo_pool,
    poolclass=NullPool,  # Warning! Don't delete this param!
)


@pytest.fixture(scope="session", autouse=True)
def event_loop(request: SubRequest) -> Generator[AbstractEventLoop, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_db() -> AsyncGenerator[None, None]:
    assert db_test_manager.engine.url == settings.db_test.url
    assert settings.db_test.url != settings.db.url

    async with db_test_manager.engine.begin() as conn:
        await conn.run_sync(BaseOrm.metadata.drop_all)
        await conn.run_sync(BaseOrm.metadata.create_all)

    async with db_test_manager.session_factory() as session:
        for mock_user in MOCK_USERS:
            stmt = insert(UserOrm).values(**mock_user)
            await session.execute(stmt)
        await session.commit()

    yield

    await db_test_manager.engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session() -> AsyncGenerator[AsyncSession, None]:
    async with db_test_manager.session_factory() as session:
        yield session


@pytest_asyncio.fixture()
async def redis_storage(redis_server: Any) -> AsyncGenerator[RedisStorage, None]:
    try:
        parse_redis_url(redis_server)
    except ValueError as e:
        raise UsageError(INVALID_URI_PATTERN.format(db="redis", uri=redis_server, err=e)) from e
    storage = RedisStorage.from_url(redis_server)
    try:
        await storage.redis.info()
    except ConnectionError as e:
        pytest.fail(str(e))
    try:
        yield storage
    finally:
        conn = await storage.redis
        await conn.flushdb()
        await storage.close()


@pytest.fixture()
def bot() -> MockedBot:
    return MockedBot()


@pytest_asyncio.fixture()
async def dispatcher() -> AsyncGenerator[Dispatcher, None]:
    dp = Dispatcher()
    await dp.emit_startup()
    try:
        yield dp
    finally:
        await dp.emit_shutdown()


@pytest_asyncio.fixture()
async def json_text() -> Any:
    return await load_json_text()
