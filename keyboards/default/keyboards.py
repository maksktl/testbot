from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

done_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Загрузить")],
        [KeyboardButton(text="◀️Назад")],
    ],
    resize_keyboard=True
)