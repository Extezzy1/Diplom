import asyncio
import os
import config
from aiogram import Router, Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from database import User, Stores, Categories, Promocodes
from dispatchers import dp_new_bot, polling_manager
import markups.admin_markup as admin_markup
import replicas.replicas_main_bot as replicas
import FSM
from polling_manager import add_bot
from sqlalchemy import select, update

commands_router = Router()


async def on_startup_load_bots(bot: Bot, sess: async_sessionmaker):
    async with sess() as session:
        request = await session.execute(select(Stores))
        bots = request.fetchall()
        for bot_ in bots:
            bot_ = bot_[0]
            print(bot_)
            for admin in config.ADMINS:
                try:
                    await bot.send_message(admin, f"Бот [{bot_.store_name}] успешно запущен!")
                except:
                    pass
                # .update_status_bot(bot_[1], "запущен")
                await add_bot(bot_.bot_token, dp_new_bot, polling_manager)


@commands_router.startup()
async def on_startup(dispatcher: Dispatcher, bot: Bot):
    asyncio.create_task(on_startup_load_bots(bot, dispatcher.workflow_data["session_maker"]))



@commands_router.message(CommandStart())
async def start(message: Message, session: AsyncSession, state: FSMContext):
    await state.clear()
    if message.from_user.id in config.ADMINS:
        await message.answer("Добрый день, выберите действие!", reply_markup=admin_markup.create_start_markup())


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
        await message.answer("Токен не прошел проверку, повторите попытку")


@commands_router.message(FSM.FSMAdmin.get_new_category_name)
async def get_new_category_name(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    category_id = data["category_id"]
    new_category_name = message.text
    await session.execute(update(Categories).where(Categories.category_id == int(category_id)).values(category_title=new_category_name))
    await session.commit()
    await state.clear()

    request = await session.execute(select(Categories).where(Categories.category_id == int(category_id)))
    store_id = request.fetchall()[0][0].store_id
    print(store_id)
    request = await session.execute(select(Categories).where(Categories.store_id == int(store_id)))
    categories = request.fetchall()
    if len(categories) > 0:
        msg = "<b>Управление категориями</b>\n\nТекущие категории:\n\n"
        for index, category in enumerate(categories, 1):
            msg += f"{index}. {category[0].category_title}\n"
    else:
        msg = "<b>Управление категориями</b>"
    await message.answer("Успешно обновил категорию\n\n" + msg, reply_markup=admin_markup.create_markup_categories(store_id))


@commands_router.message(FSM.FSMAdmin.get_category_name)
async def get_category_name(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    store_id = data["store_id"]
    category_name = message.text
    request = await session.execute(select(Categories).where(Categories.category_title == category_name, Categories.store_id == int(store_id)))
    is_category_in_db = bool(len(request.fetchall()))
    if is_category_in_db:
        await message.answer("Наименование категории должно быть уникальным! Повторите ввод")
        return

    await session.merge(Categories(category_id_fk=None, store_id=int(data["store_id"]), category_title=category_name, ))
    await session.commit()
    await state.clear()

    request = await session.execute(select(Categories).where(Categories.store_id == int(data["store_id"])))
    categories = request.fetchall()
    if len(categories) > 0:
        msg = "<b>Управление категориями</b>\n\nТекущие категории:\n\n"
        for index, category in enumerate(categories, 1):
            msg += f"{index}. {category[0].category_title}\n"
    else:
        msg = "<b>Управление категориями</b>"
    await message.answer("Успешно добавил категорию\n\n" + msg, reply_markup=admin_markup.create_markup_categories(data["store_id"]))


@commands_router.message(FSM.FSMAdmin.get_promocode_name)
async def get_promocode_name(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()

    if message.text == replicas.cancel:
        await message.answer(text="Управление промокодами", reply_markup=admin_markup.create_markup_promocodes(data["store_id"]))
        return

    promocode_name = message.text.strip()

    request = await session.execute(select(Promocodes).where(Promocodes.promocode_title == promocode_name, Promocodes.store_id == int(data["store_id"])))
    promocodes_in_db_with_current_name = request.fetchall()
    if len(promocodes_in_db_with_current_name) > 0:
        await message.answer("Промокод с данным наименование уже есть! Введите другое наименование")
        return


    data["promocode_name"] = promocode_name
    await state.set_data(data)
    await message.answer("Теперь процент скидки для данного промокода", reply_markup=admin_markup.create_markup_cancel())
    await state.set_state(FSM.FSMAdmin.get_promocode_discount)


@commands_router.message(FSM.FSMAdmin.get_promocode_discount)
async def get_promocode_discount(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()

    if message.text == replicas.cancel:
        await message.answer(text="Управление промокодами", reply_markup=admin_markup.create_markup_promocodes(data["store_id"]))
        return

    if not message.text.isdigit():
        await message.answer("Процент скидки должен быть целым числом! Повторите ввод", reply_markup=admin_markup.create_markup_cancel())
        return

    if not(0 < int(message.text.strip()) <= 100):
        await message.answer("Процент скидки не может быть меньше нуля или больше 100! Повторите ввод",
                             reply_markup=admin_markup.create_markup_cancel())
        return


    promocode_discount = message.text.strip()
    promocode_name = data["promocode_name"]
    store_id = data["store_id"]
    await session.merge(Promocodes(store_id=int(store_id), promocode_title=promocode_name, discount_percent=int(promocode_discount)))
    await session.commit()
    await message.answer("Успешно добавил новый промокод!", reply_markup=admin_markup.create_markup_promocodes(data["store_id"]))
    await state.clear()


@commands_router.message(FSM.FSMAdmin.get_new_promocode_discount)
async def get_new_promocode_discount(message: Message, state: FSMContext, session: AsyncSession):

    data = await state.get_data()
    request = await session.execute(select(Promocodes.store_id).where(Promocodes.promocode_id == int(data["promocode_id"])))
    store_id = request.fetchmany(1)[0][0]
    print(store_id)
    if message.text == replicas.cancel:
        await message.answer(text="Управление промокодами", reply_markup=admin_markup.create_markup_promocodes(store_id))
        return

    if not message.text.isdigit():
        await message.answer("Процент скидки должен быть целым числом! Повторите ввод", reply_markup=admin_markup.create_markup_cancel())
        return

    if not (0 < int(message.text.strip()) <= 100):
        await message.answer("Процент скидки не может быть меньше нуля или больше 100! Повторите ввод",
                             reply_markup=admin_markup.create_markup_cancel())
        return

    promocode_discount = message.text.strip()
    await session.execute(update(Promocodes).where(Promocodes.promocode_id == int(data["promocode_id"])).values(discount_percent=int(promocode_discount)))
    await session.commit()
    await message.answer("Успешно обновил процент скидки!", reply_markup=admin_markup.create_markup_promocodes(store_id))
    await state.clear()


@commands_router.message(FSM.FSMAdmin.get_product_name)
async def get_product_name(message: Message):
    pass



@commands_router.message()
async def all_messages(message: Message, bot: Bot, state: FSMContext, session: AsyncSession):
    if message.text == replicas.create_store:
        await message.answer("""🤖️ Чтобы создать новый магазин, мне нужен токен
➀ Перейдите в @BotFather

➁ Отправьте в @BotFather команду - /newbot

➂ Придумайте название и юзернейм для вашего бота, например: "Новости" | @newsbot

➃ @BotFather выдаст вам токен бота, пример токена: 5827254996:AAEBu9108achvHoWvPmvr6kueDgmFpJMjHo

➄ Пришлите токен нового бота сюда ☟""")
        await state.set_state(FSM.FSMAdmin.get_token_bot)


    elif message.text == replicas.my_stores:
        request = await session.execute(select(Stores))
        stores = request.fetchall()
        if len(stores) == 0:
            await message.answer("Список магазинов пуст!", reply_markup=admin_markup.create_start_markup())
            return

        await message.answer("Ваши магазины", reply_markup=admin_markup.create_markup_stores(stores))


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
