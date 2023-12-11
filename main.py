import asyncio
import logging

import aiogram

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker
from middlewares import DbSessionMiddleware
from handlers.main_bot.commands import commands_router
from handlers.main_bot.callbacks import callbacks_router
import config
from database import BaseModel, create_async_engine
from dispatchers import dp_new_bot, polling_manager
import logging
from session_maker_ import session_maker
logger = logging.getLogger(__name__)


async def main():

    bot = Bot(token=config.bot_token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(callbacks_router, commands_router)
    dp.update.middleware(DbSessionMiddleware(session_pool=session_maker))
    # dp.callback_query
    # await proceed_schemas(async_engine, BaseModel.metadata)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, dp_new_bot=dp_new_bot, polling_manager=polling_manager, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Exit")