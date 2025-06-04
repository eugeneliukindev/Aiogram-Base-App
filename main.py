import asyncio
import logging

import redis.asyncio as aredis
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from app.config import settings
from app.core import db_manager
from app.handlers.commands import router as commands_router
from app.middlewares import SessionDepMiddleware
from app.utils.logger import configure_logging

log = logging.getLogger(__name__)


async def on_shutdown(bot: Bot) -> None:
    await db_manager.dispose()
    log.info("Shutdown complete")


async def main(
    bot_token: str = settings.bot.token,
    redis_host: str = settings.redis.host,
    redis_port: int = settings.redis.port,
) -> None:
    log.info("Starting Bot...")
    redis = aredis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.delete_webhook(drop_pending_updates=True)

    storage = RedisStorage(redis=redis)

    dp = Dispatcher(storage=storage)
    dp.shutdown.register(on_shutdown)

    dp.include_routers(commands_router)

    dp.update.outer_middleware.register(SessionDepMiddleware())

    await dp.start_polling(bot)


if __name__ == "__main__":
    configure_logging()
    asyncio.run(main())
