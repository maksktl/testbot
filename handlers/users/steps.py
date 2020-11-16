from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup

from data.steps_data import bull_remont_types, exc_remont_types
from handlers.users.start import cq_start, start
from keyboards.default.keyboards import done_button
from keyboards.inline.keyboards import bulldozer_num, excavator_num, exc_remont_list, bull_remont_list, back_button
from loader import dp, bot
from states.user_state import UserStep


@dp.callback_query_handler(text="bulldozers")
async def bulldozers(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(tech="Бульдозер")
    await call.message.answer("✅ Введите номер техники для <i>Бульдозера</i>:", reply_markup=back_button("start"))
    await UserStep.tech_number.set()


@dp.callback_query_handler(text="excavator")
async def excavator(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(tech="Эксковатор")
    await call.message.answer("✅ Введите номер техники для <i>Эксковатора</i>:", reply_markup=back_button("start"))
    await UserStep.tech_number.set()


@dp.message_handler(state=UserStep.tech_number)
async def choose_type(message: types.Message, state: FSMContext):
    """
    Обработка введенного вручную номера техники и отправка сообщения с выбором ремонта.
    """
    # Получаем номер техники
    tech = (await state.get_data()).get('tech')
    if tech is None:
        # Если не получилось, то возвращаем в начальное меню
        await state.reset_state(with_data=True)
        await start(message)
        return
    # клавиатура, которая будет показывать список ремонтов
    keyboard = InlineKeyboardMarkup()
    if tech == "Бульдозер":
        # Если техника бульдозер, то клавиатура ремонтов для бульдозера
        keyboard = bull_remont_list
    elif tech == "Эксковатор":
        # Если техника Эксковатор, то клавиатура ремнотов для эксковатора
        keyboard = exc_remont_list
    else:
        # Если не то и не другое, то случилась ошибка ввода данных, возвращем в главное меню
        await state.reset_state(with_data=True)
        await start(message)
        return

    number = message.text
    # сохраняем номер техники в контекст
    await state.update_data(number=number)
    await message.answer("⚙️Выберите ремонт для Бульдозера:", reply_markup=keyboard)

    # далее не нужен FSM, так как будет использоваться callback.
    await state.reset_state(with_data=False)


@dp.callback_query_handler(text_contains="bull_remont")
async def bull_remont(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data.get('tech') is None or data.get('tech') != "Бульдозер" or data.get('number')[0] != 'Б':
        await state.reset_state(with_data=True)
        await cq_start(call)
        return

    remont_type = bull_remont_types[int(call.data.split(':')[1])]
    await state.update_data(remont_type=remont_type)
    await call.message.answer("📸 Пришлите фото до, затем нажмите на кнопку ✅Загрузить", reply_markup=done_button)
    await UserStep.before.set()


@dp.callback_query_handler(text_contains="exc_remont")
async def exc_remont(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data.get('tech') is None or data.get('tech') != "Эксковатор" or data.get('number')[0] != 'Э':
        await state.reset_state(with_data=True)
        await cq_start(call)
        return

    remont_type = exc_remont_types[int(call.data.split(':')[1])]
    await state.update_data(remont_type=remont_type)
    await call.message.answer("📸 Пришлите фото до, затем нажмите на кнопку ✅Загрузить", reply_markup=done_button)
    await UserStep.before.set()


@dp.message_handler(text="◀️Назад", state=UserStep.before)
async def back_before(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=False)
    await state.update_data(photo_before=None)
    await message.answer("Вы вернулись назад", reply_markup=types.ReplyKeyboardRemove())
    tech = (await state.get_data()).get('tech')
    if tech == 'Бульдозер':
        await message.answer('⚙️Выберите ремонт для Бульдозера:', reply_markup=bull_remont_list)
        return
    await message.answer("⚙️Выберите ремонт для Эксковатора:", reply_markup=exc_remont_list)


@dp.message_handler(text="◀️Назад", state=UserStep.after)
async def back_after(message: types.Message, state: FSMContext):
    await UserStep.before.set()
    await state.update_data(photo_after=None)
    await message.answer("Вы вернулись назад", reply_markup=types.ReplyKeyboardRemove())
    await message.answer("📸 Пришлите фото до, затем нажмите на кнопку ✅Загрузить", reply_markup=done_button)
