from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from utils.db_api.schemas.user import User


class AccessMiddleware(BaseMiddleware):

    def __init__(self):
        super().__init__()

    async def on_pre_process_message(self, message: types.Message, data: dict, *arg, **kwargs):
        data['user'] = await User().get_or_create(message.from_user)

    async def on_pre_process_callback_query(self, callback_query: types.CallbackQuery, data: dict, *arg, **kwargs):
        data['user'] = await User().get_or_create(callback_query.from_user)

