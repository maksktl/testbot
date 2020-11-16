from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStep(StatesGroup):
    tech_number = State()
    remont_type = State()
    before = State()
    after = State()
