from aiogram import Dispatcher
from aiogram.utils.chat_action import ChatActionMiddleware

from handlers.sub_bot.commands import commands_router
from handlers.sub_bot.callbacks import callbacks_router
from middlewares import DbSessionMiddleware
from polling_manager import PollingManager
from session_maker_ import session_maker


dp_new_bot = Dispatcher(session_pool=session_maker)
dp_new_bot.update.middleware(DbSessionMiddleware(session_pool=session_maker))

# dp_new_bot.message.middleware(ChatActionMiddleware())

dp_new_bot.include_routers(commands_router, callbacks_router)

polling_manager = PollingManager()
