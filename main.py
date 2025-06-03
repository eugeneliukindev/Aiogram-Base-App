import asyncio

import redis.asyncio as aredis
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from app.config import settings
from app.middlewares import SessionDepMiddleware
from app.utils.logger import configure_logging


async def main(
    bot_token: str = settings.bot.token,
    redis_host: str = settings.redis.host,
    redis_port: int = settings.redis.port,
) -> None:
    redis = aredis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.delete_webhook(drop_pending_updates=True)

    storage = RedisStorage(redis=redis)

    dp = Dispatcher(storage=storage)

    dp.update.outer_middleware.register(SessionDepMiddleware())

    await dp.start_polling(bot)


if __name__ == "__main__":
    configure_logging()
    asyncio.run(main())
