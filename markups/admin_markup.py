from aiogram import types
import replicas.replicas_main_bot


def create_start_markup():
    kb = [
        [types.KeyboardButton(text=replicas.replicas_main_bot.create_store)],
        [types.KeyboardButton(text=replicas.replicas_main_bot.my_stores)],
    ]
    markup = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return markup
