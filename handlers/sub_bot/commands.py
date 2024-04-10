from aiogram import Router, Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.handlers.message import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import BotCommand, BotCommandScopeDefault
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import markups.client_markup as client_markup
import FSM
from database import User, UsersStore, Stores, Referrals

commands_router = Router()


# async def on_startup_load_bots(bot: Bot):
#     bots = db.get_active_bots()
#     for bot_ in bots:
#         if bot_[3] == "запущен":
#             for admin in config.ADMINS:
#                 try:
#                     await bot.send_message(admin, f"Бот [{bot_[2]}] успешно запущен!")
#                 except:
#                     pass
#             db.update_status_bot(bot_[1], "запущен")
#             await add_bot(bot_[1], dp_new_bot, polling_manager)
#
#
# @commands_router.startup()
# async def on_startup(dispatcher: Dispatcher, bot: Bot):
#     asyncio.create_task(on_startup_load_bots(bot))
#
#
@commands_router.message(CommandStart())
async def start(message: Message, session: AsyncSession, bot: Bot):
    result = await session.execute(select(User).where(User.user_id == message.from_user.id))
    user = result.one_or_none()
    if user is None:
        await session.merge(User(user_id=message.from_user.id, first_name=message.from_user.first_name))
        await session.commit()
    username = (await bot.get_me()).username
    request = await session.execute(select(Stores.store_id).where(Stores.store_name == username))
    store_id = request.fetchmany(1)[0][0]
    request = await session.execute(select(UsersStore).where(UsersStore.user_id == message.from_user.id, UsersStore.store_id == store_id))
    is_added = bool(len(request.fetchall()))
    if not is_added:
        await session.merge(UsersStore(user_id=message.from_user.id, store_id=store_id))
        await session.commit()

    if len(message.text.split(" ")) == 2:
        referrer_id = message.text.split(" ")[1]
        if referrer_id.isdigit():
            request = await session.execute(select(Referrals).where(Referrals.user_id_sender == int(referrer_id), Referrals.user_id_invited == message.from_user.id))
            is_referral = bool(len(request.fetchall()))
            if not is_referral:
                await session.merge(Referrals(user_id_sender=int(referrer_id), user_id_invited=message.from_user.id))
                await bot.send_message(chat_id=referrer_id, text=f'У вас появился новый реферал - <a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a>')
                await session.commit()
    await message.answer("Главное меню", reply_markup=client_markup.create_start_markup())


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command="start",
            description="Запустить бота",
        ),
    ]

    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())


# # async def on_bot_startup(bot: Bot):
# #     await set_commands(bot)
# #     await bot.send_message(chat_id=ADMIN_ID, text="Bot started!")
# #
# #
# # async def on_bot_shutdown(bot: Bot):
# #     await bot.send_message(chat_id=ADMIN_ID, text="Bot shutdown!")
# #
# #
# # async def on_startup(bots: List[Bot]):
# #     for bot in bots:
# #         await on_bot_startup(bot)
# #
# #
# # async def on_shutdown(bots: List[Bot]):
# #     for bot in bots:
# #         await on_bot_shutdown(bot)
# #
