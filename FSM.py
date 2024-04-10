from aiogram.fsm.state import StatesGroup, State


class FSMAdmin(StatesGroup):
    get_token_bot = State()

    # Category
    get_category_name = State()
    get_new_category_name = State()

    # Promocode
    get_promocode_name = State()
    get_promocode_discount = State()
    get_new_promocode_discount = State()

    # Product
    get_product_name = State()
    get_new_product_name = State()

