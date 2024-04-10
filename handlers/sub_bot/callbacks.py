from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
import FSM
import markups.client_markup as client_markup


callbacks_router = Router()


@callbacks_router.callback_query(lambda c: c.data == "get_my_ref_link")
async def get_my_ref_link(callback: CallbackQuery, bot: Bot):
    shop_username = (await bot.get_me()).username
    await callback.message.answer(f"Ваша реферальная ссылка - <b>https://t.me/{shop_username}?start={callback.from_user.id}</b>",
                                  reply_markup=client_markup.create_start_markup())

