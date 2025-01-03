from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from data import config


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        return int(message.from_user.id) in config.ADMINS
    async def check_two(self, call: types.CallbackQuery):
        return int(call.from_user.id) in config.ADMINS
    async def check_three(self, call: types.InlineQuery):
        return int(call.from_user.id) in config.ADMINS