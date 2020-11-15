from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.start import cq_start, start
from loader import dp


@dp.callback_query_handler(state='*')
async def error_call(call: types.CallbackQuery, state: FSMContext):
    await state.reset_state(with_data=True)
    await cq_start(call)


@dp.message_handler(state='*')
async def error_message(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=True)
    await start(message)
