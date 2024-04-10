from aiogram import types
import config


def create_start_markup():
    kb= [
        [types.InlineKeyboardButton(text="Мои заказы", callback_data="my_orders"), types.InlineKeyboardButton(text="Каталог", callback_data="catalog")],
        [types.InlineKeyboardButton(text="Ссылка для приглашения", callback_data="get_my_ref_link")]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)


