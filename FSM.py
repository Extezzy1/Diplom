from aiogram.fsm.state import StatesGroup, State


class FSMAdmin(StatesGroup):
    get_token_bot = State()

