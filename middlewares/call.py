from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import MessageError


class CallAnswerMiddleware(BaseMiddleware):

    def __init__(self):
        super().__init__()

    async def on_post_process_callback_query(self, call: types.CallbackQuery, data: dict, *arg, **kwargs):
        try:
            await call.message.delete()
        except MessageError:
            pass
