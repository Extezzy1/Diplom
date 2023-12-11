from aiogram import types
import config


def create_markup_buy_rate():
    buttons = [
        [types.InlineKeyboardButton(text=f"1 месяц - {config.month_1_price / 100}₽", callback_data="buy_rate_1_month")],
        [types.InlineKeyboardButton(text=f"6 месяцев - {config.month_6_price / 100}₽", callback_data="buy_rate_6_month")],
        [types.InlineKeyboardButton(text=f"12 месяцев - {config.month_12_price / 100}₽", callback_data="buy_rate_12_month")],
        [types.InlineKeyboardButton(text="Главное меню", callback_data="main_menu")],
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup


def create_markup_main_menu():
    buttons = [
        [types.InlineKeyboardButton(text="Памятка для пациентов", callback_data="memo")],
        [types.InlineKeyboardButton(text="Подбор кодов и диагнозов", callback_data="select_of_code")],
        [types.InlineKeyboardButton(text="Атлас анатомии", callback_data="atlas")],
        [types.InlineKeyboardButton(text="Личный кабинет", callback_data="personal_account")],
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup


def create_markup_personal_account():
    buttons = [
        [types.InlineKeyboardButton(text="Изменить данные аккаунта (ФИО, телефон, почта)", callback_data="change_data_account")],
        [types.InlineKeyboardButton(text="Продлить подписку", callback_data="extend_subscribe")],
        [types.InlineKeyboardButton(text="Назад", callback_data="back")],

    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup


def create_markup_change_data_account():
    buttons = [
        [types.InlineKeyboardButton(text="ФИО", callback_data="change_fio")],
        [types.InlineKeyboardButton(text="Телефон", callback_data="change_phone")],
        [types.InlineKeyboardButton(text="Почта", callback_data="change_email")],
        [types.InlineKeyboardButton(text="Главное меню", callback_data="main_menu")],
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup


def create_markup_select_of_code():
    buttons = [
        [types.InlineKeyboardButton(text="Выбрать процедуру", switch_inline_query_current_chat="")],
        [types.InlineKeyboardButton(text="Главное меню", callback_data="main_menu")],
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup


def create_markup_atlas():
    buttons = [
        [types.InlineKeyboardButton(text="Выбрать тему", switch_inline_query_current_chat="")],
        [types.InlineKeyboardButton(text="Главное меню", callback_data="main_menu")],
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup


def create_markup_memo():
    buttons = [
        [types.InlineKeyboardButton(text="Выбрать процедуру", switch_inline_query_current_chat="")],
        [types.InlineKeyboardButton(text="Главное меню", callback_data="main_menu")],
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup


def create_markup_memo_recommendations():
    buttons = [
        [types.InlineKeyboardButton(text="Добавить комментарий", callback_data="add_comment")],
        [types.InlineKeyboardButton(text="Подтвердить", callback_data="accept")],
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup


def create_markup_memo_create_pdf():
    buttons = [
        [types.InlineKeyboardButton(text="Сформировать файл", callback_data="create_pdf")],
        [types.InlineKeyboardButton(text="Добавление процедуры", callback_data="add_procedure")],
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup


def create_markup_subprocedures(sub_procedures):
    buttons = [[types.InlineKeyboardButton(text=procedure[0].procedure_subname, callback_data=f"sub_procedure_{procedure[0].sub_procedure_id}")] for procedure in sub_procedures]
    buttons.append(
        [types.InlineKeyboardButton(text="Главное меню", callback_data="main_menu")],
    )
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup


def create_markup_link_to_channel():
    buttons = [
        [types.InlineKeyboardButton(text="Подписаться", url=config.CHANNEL_LINK)],
        [types.InlineKeyboardButton(text="Готово", callback_data="check_subscribe")],
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup


def create_markup_back_to_main_menu():
    buttons = [
        [types.InlineKeyboardButton(text="Главное меню", callback_data="main_menu")],
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup



def create_markup_payment(url, bill_id):
    buttons = [
        [types.InlineKeyboardButton(text="Оплатить", url=url)],
        [types.InlineKeyboardButton(text="Я оплатил(а)", callback_data=f"payment_successful_{bill_id}")]

    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup