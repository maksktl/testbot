from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.default.keyboards import done_button
from loader import dp
from states.user_state import UserStep
from utils.db_api.schemas.photo_after import PhotoAfter
from utils.db_api.schemas.photo_before import PhotoBefore
from utils.db_api.schemas.user import User


@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=UserStep.before)
async def photo_before(message: types.Message, state: FSMContext):
    data = (await state.get_data()).get('photo_before')
    if data is None:
        data = []
    data.append(message.photo[-1].file_id)
    await state.update_data(photo_before=data)


@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=UserStep.after)
async def photo_after(message: types.Message, state: FSMContext):
    data = (await state.get_data()).get('photo_after')
    if data is None:
        data = []
    data.append(message.photo[-1].file_id)
    await state.update_data(photo_after=data)


@dp.message_handler(text="✅ Загрузить", state=UserStep.before)
async def upload_before(message: types.Message, state: FSMContext):
    data = (await state.get_data()).get('photo_before')
    if data is None or data == []:
        await message.answer("⚠️Вы не загрузили фото!")
        return

    await UserStep.after.set()
    await message.answer("📸 Пришлите фото после, затем нажмите на кнопку ✅Загрузить", reply_markup=done_button)


@dp.message_handler(text="✅ Загрузить", state=UserStep.after)
async def upload_after(message: types.Message, state: FSMContext, user: User):
    data = (await state.get_data()).get('photo_after')
    if data is None or data == []:
        await message.answer("⚠️Вы не загрузили фото!")
        return

    # TODO: загрузка всего в базу данных
    info = (await state.get_data())
    await PhotoBefore.create_photo(user.user_id, info.get('tech'), info.get('number'), info.get('remont_type'),
                                   info.get('photo_before'))
    await PhotoAfter.create_photo(user.user_id, info.get('tech'), info.get('number'), info.get('remont_type'),
                                   info.get('photo_after'))
    await User.add_photo_before(user.user_id, len(info.get('photo_before')))
    await User.add_photo_after(user.user_id, len(info.get('photo_after')))
    await state.reset_state(with_data=True)
    await message.answer("✅ Вы успешно загрузили фото до/после!", reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Нажмите на главное меню чтобы загрузить фото еще раз.", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🏠 Главное меню", callback_data="start")]]
    ))
