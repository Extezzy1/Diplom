from aiogram import types
import replicas.replicas_main_bot


def create_markup_cancel():
    kb = [
        [types.InlineKeyboardButton(text=replicas.replicas_main_bot.cancel, callback_data="cancel")],
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb, resize_keyboard=True)
    return markup


def create_start_markup():
    kb = [
        [types.KeyboardButton(text=replicas.replicas_main_bot.create_store)],
        [types.KeyboardButton(text=replicas.replicas_main_bot.my_stores)],
    ]
    markup = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return markup


def create_markup_stores(stores):
    kb = []
    for store in stores:
        store = store[0]
        kb.append([types.InlineKeyboardButton(text=store.store_name, callback_data=f"store_{store.store_id}")])
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)
    return markup


def create_markup_manage_store(store_id):
    kb = [
        [types.InlineKeyboardButton(text="Категории", callback_data=f"categories_{store_id}"),
         types.InlineKeyboardButton(text="Статистика", callback_data=f"statistics_{store_id}")],
        [types.InlineKeyboardButton(text="Промокоды", callback_data=f"promocodes_{store_id}"),
         types.InlineKeyboardButton(text="Товары", callback_data=f"products_{store_id}")],
        [types.InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_list_stores")]
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)
    return markup


def create_markup_categories(store_id):
    kb = [
        [types.InlineKeyboardButton(text="Добавить", callback_data=f"add_category_{store_id}"),
         types.InlineKeyboardButton(text="Удалить", callback_data=f"delete_categories_{store_id}")],
        [types.InlineKeyboardButton(text="Редактировать", callback_data=f"edit_categories_{store_id}")],
         [types.InlineKeyboardButton(text="⏪ Главное меню", callback_data=f"main_menu_{store_id}")],
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)
    return markup


def create_markup_delete_categories(store_id, categories):
    kb = []
    for category in categories:
        kb.append([types.InlineKeyboardButton(text=category[0].category_title, callback_data=f"delete_category_{category[0].category_id}")])
    kb.append([types.InlineKeyboardButton(text="🔙 Назад", callback_data=f"back_to_categories_{store_id}")])
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)
    return markup


def create_markup_edit_categories(store_id, categories):
    kb = []
    for category in categories:
        kb.append([types.InlineKeyboardButton(text=category[0].category_title, callback_data=f"edit_category_{category[0].category_id}")])
    kb.append([types.InlineKeyboardButton(text="🔙 Назад", callback_data=f"back_to_categories_{store_id}")])
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)
    return markup


def create_markup_promocodes(store_id):
    kb = [
        [types.InlineKeyboardButton(text="Добавить", callback_data=f"add_promocode_{store_id}"),
         types.InlineKeyboardButton(text="Удалить", callback_data=f"delete_promocodes_{store_id}")],
        [types.InlineKeyboardButton(text="Активные промокоды", callback_data=f"active_promocodes_{store_id}"),
         types.InlineKeyboardButton(text="Установить скидку", callback_data=f"set_discount_{store_id}")],
         [types.InlineKeyboardButton(text="⏪ Главное меню", callback_data=f"main_menu_{store_id}")],
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)
    return markup


def create_markup_delete_promocodes(promocodes, store_id):

    kb = []
    for promocode in promocodes:
        kb.append([types.InlineKeyboardButton(text=promocode.promocode_title, callback_data=f"delete_promocode_{promocode.promocode_id}")])
    kb.append([types.InlineKeyboardButton(text=replicas.replicas_main_bot.back, callback_data=f"back_promocodes_{store_id}")])
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)
    return markup


def create_markup_show_active_promocodes(store_id):
    kb = [[types.InlineKeyboardButton(text=replicas.replicas_main_bot.back, callback_data=f"back_promocodes_{store_id}")]]
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)
    return markup


def create_markup_set_discount_promocode(promocodes, store_id):

    kb = []
    for promocode in promocodes:
        kb.append([types.InlineKeyboardButton(text=promocode.promocode_title, callback_data=f"set_promocode_discount_{promocode.promocode_id}")])
    kb.append([types.InlineKeyboardButton(text=replicas.replicas_main_bot.back, callback_data=f"back_promocodes_{store_id}")])
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)
    return markup


def create_markup_products(store_id):
    kb = [
        [types.InlineKeyboardButton(text="Добавить", callback_data=f"add_product_{store_id}"),
         types.InlineKeyboardButton(text="Удалить", callback_data=f"delete_products_{store_id}")],
        [types.InlineKeyboardButton(text="Редактировать", callback_data=f"edit_products_{store_id}")],
         [types.InlineKeyboardButton(text="⏪ Главное меню", callback_data=f"main_menu_{store_id}")],
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)
    return markup


def create_markup_delete_products(store_id, products):
    kb = []
    for product in products:
        kb.append([types.InlineKeyboardButton(text=product[0].category_title, callback_data=f"delete_product_{product[0].product_id}")])
    kb.append([types.InlineKeyboardButton(text="🔙 Назад", callback_data=f"back_to_products_{store_id}")])
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)
    return markup


def create_markup_edit_products(store_id, products):
    kb = []
    for product in products:
        kb.append([types.InlineKeyboardButton(text=product[0].category_title, callback_data=f"edit_product_{product[0].category_id}")])
    kb.append([types.InlineKeyboardButton(text="🔙 Назад", callback_data=f"back_to_products_{store_id}")])
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)
    return markup