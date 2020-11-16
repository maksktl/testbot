from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.inline.keyboards import tech_type
from loader import dp


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    await message.answer("🚜 Выберите тип техники:", reply_markup=tech_type)


@dp.callback_query_handler(text="start", state="*")
async def cq_start(call: types.CallbackQuery, state: FSMContext):
    await state.reset_state(with_data=True)
    await call.message.answer("🚜 Выберите тип техники:", reply_markup=tech_type)
