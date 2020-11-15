from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStep(StatesGroup):
    before = State()
    after = State()
