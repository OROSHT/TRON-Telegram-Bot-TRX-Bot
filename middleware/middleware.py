from aiogram import Dispatcher
from aiogram.dispatcher.handler import CancelHandler 
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from loader import db
from data import config

class UserBanned(BaseMiddleware):
    async def on_process_message(self, message: Message, data: dict):
        if message.from_user.id in config.ADMINS:
            return
        user = await db.get_user(message.from_user.id)

        if user and user.banned == 1:
            await message.answer(
                '<b>🔥 Вы заблокированы</b>'
            )
            raise CancelHandler

    async def on_process_callback_query(self, call: CallbackQuery, data: dict):
        if call.from_user.id in config.ADMINS:
            return
        user = await db.get_user(call.from_user.id)
        if user and user.banned == 1:
            await call.answer(
                '🔥 Вы заблокированы',
                show_alert=True
            )
            raise CancelHandler