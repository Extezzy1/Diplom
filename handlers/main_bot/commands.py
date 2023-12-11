import asyncio
import os
import config
from aiogram import Router, Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database import User, Stores
from dispatchers import dp_new_bot, polling_manager
import markups.admin_markup as admin_markup
import replicas.replicas_main_bot as replicas
import FSM
from polling_manager import add_bot
from sqlalchemy import select, update

commands_router = Router()


async def on_startup_load_bots(bot: Bot, session: AsyncSession):
    # request = await session.execute(select(Stores.bot_token))
    # bots = request.fetchall()
    # for bot_ in bots:
    #     for admin in config.ADMINS:
    #             try:
    #                 await bot.send_message(admin, f"Бот [{bot_[2]}] успешно запущен!")
    #             except:
    #                 pass
    #         db.update_status_bot(bot_[1], "запущен")
    #         await add_bot(bot_[1], dp_new_bot, polling_manager)
    pass

# @commands_router.startup()
# async def on_startup(dispatcher: Dispatcher, bot: Bot, session: AsyncSession):
#     asyncio.create_task(on_startup_load_bots(bot, session))


@commands_router.message(CommandStart())
async def start(message: Message, session: AsyncSession):

    result = await session.execute(select(User).where(User.user_id == message.from_user.id))
    user = result.one_or_none()
    if user is None:
        await session.merge(User(user_id=message.from_user.id, first_name=message.from_user.first_name))
        await session.commit()

    if message.from_user.id in config.ADMINS:
        await message.answer("Привет!", reply_markup=admin_markup.create_start_markup())


@commands_router.message(FSM.FSMAdmin.get_token_bot)
async def get_token_bot(message: Message, state: FSMContext, session: AsyncSession):
    if len(message.text.split(":")) == 2 and message.text.split(":")[0].isdigit():

        token = message.text
        result, username, bot_id = await add_bot(token, dp_new_bot, polling_manager)
        if bot_id:
            await session.merge(Stores(user_id_creator=message.from_user.id, store_name=username, bot_token=token))
            await session.commit()
            await message.answer("Магазин успешно создан!", reply_markup=admin_markup.create_start_markup())
        else:
            await message.answer("Не удалось запустить магазин", reply_markup=admin_markup.create_start_markup())
        await state.clear()
    else:
        await message.answer("Токен не прошел проверку, повтори попытку")


@commands_router.message()
async def all_messages(message: Message, bot: Bot, state: FSMContext):
    if message.text == replicas.create_store:
        await message.answer("""🤖️ Чтобы создать новый магазин, мне нужен токен
➀ Перейдите в @BotFather

➁ Отправьте в @BotFather команду - /newbot

➂ Придумайте название и юзернейм для вашего бота, например: "Новости" | @newsbot

➃ @BotFather выдаст вам токен бота, пример токена: 5827254996:AAEBu9108achvHoWvPmvr6kueDgmFpJMjHo

➄ Пришлите токен нового бота сюда ☟""")
        await state.set_state(FSM.FSMAdmin.get_token_bot)

    # elif message.text == replicas.my_stores:
    #     bots = db.get_bots()
    #     if len(bots) == 0:
    #         await message.answer("У вас нет персонажей")
    #         return
    #
    #     for bot in bots:
    #         msg = f"[{bot[3]}] - @{bot[2]}\n"
    #         await message.answer(msg, reply_markup=admin_markup.create_markup_start_stop_bot(bot[3], bot[0]))
    #

# async def set_commands(bot: Bot):
#     commands = [
#         BotCommand(
#             command="add_bot",
#             description="add bot, usage '/add_bot 123456789:qwertyuiopasdfgh'",
#         ),
#         BotCommand(
#             command="stop_bot",
#             description="stop bot, usage '/stop_bot 123456789'",
#         ),
#     ]
#
#     await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())


# async def on_bot_startup(bot: Bot):
#     await set_commands(bot)
#     await bot.send_message(chat_id=ADMIN_ID, text="Bot started!")
#
#
# async def on_bot_shutdown(bot: Bot):
#     await bot.send_message(chat_id=ADMIN_ID, text="Bot shutdown!")
#
#
# async def on_startup(bots: List[Bot]):
#     for bot in bots:
#         await on_bot_startup(bot)
#
#
# async def on_shutdown(bots: List[Bot]):
#     for bot in bots:
#         await on_bot_shutdown(bot)
#
