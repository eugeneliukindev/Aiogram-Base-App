import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from src.config import settings
from src.core import db_manager
from src.handlers.commands import router as commands_router
from src.middlewares import SessionDepMiddleware, TextsDepMiddleware
from src.utils.logger import configure_logging

log = logging.getLogger(__name__)


async def on_shutdown(bot: Bot) -> None:
    await db_manager.engine.dispose()
    log.info("Shutdown complete")


async def main(
    bot_token: str = settings.bot.token,
    redis_url: str = settings.redis.url,
) -> None:
    log.info("Starting Bot...")
    bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.delete_webhook(drop_pending_updates=True)

    storage: RedisStorage = RedisStorage.from_url(url=redis_url)

    dp = Dispatcher(storage=storage)
    dp.shutdown.register(on_shutdown)

    dp.include_routers(commands_router)

    commands_router.message.middleware(TextsDepMiddleware())

    dp.update.outer_middleware.register(SessionDepMiddleware())

    await dp.start_polling(bot)


if __name__ == "__main__":
    configure_logging()
    asyncio.run(main())
