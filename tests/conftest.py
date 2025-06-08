import asyncio

import pytest
import pytest_asyncio
from _pytest.config import UsageError
from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio.connection import parse_url as parse_redis_url
from redis.exceptions import ConnectionError
from sqlalchemy import NullPool

from app.config import settings
from app.core.db_manager import DatabaseManager
from app.core.models import BaseOrm
from tests.mock_bot import MockedBot

SKIP_MESSAGE_PATTERN = 'Need "--{db}" option with {db} URI to run'
INVALID_URI_PATTERN = "Invalid {db} URI {uri!r}: {err}"

db_test_manager = DatabaseManager(
    url=settings.db_test.url,
    echo=settings.db_test.echo,
    echo_pool=settings.db_test.echo_pool,
    poolclass=NullPool,  # Warning! Don't delete this param!
)


@pytest_asyncio.fixture(scope="session", autouse=True)
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_db():
    assert db_test_manager.engine.url == settings.db_test.url
    async with db_test_manager.engine.begin() as conn:
        await conn.run_sync(BaseOrm.metadata.drop_all)
        await conn.run_sync(BaseOrm.metadata.create_all)
    yield
    await db_test_manager.engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session():
    async with db_test_manager.session_factory() as session:
        yield session


@pytest.fixture()
async def redis_storage(redis_server):
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
def bot():
    return MockedBot()


@pytest.fixture()
async def dispatcher():
    dp = Dispatcher()
    await dp.emit_startup()
    try:
        yield dp
    finally:
        await dp.emit_shutdown()
