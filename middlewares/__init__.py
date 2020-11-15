from aiogram import Dispatcher

from .access import AccessMiddleware
from .call import CallAnswerMiddleware


def setup(dp: Dispatcher):
    dp.middleware.setup(CallAnswerMiddleware())
    dp.middleware.setup(AccessMiddleware())
