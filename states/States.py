from aiogram.dispatcher.filters.state import State, StatesGroup

class GetTrx(StatesGroup):
    amount = State()

class ChangeTrx(StatesGroup):
    adres = State()

class UpdateBalance(StatesGroup):
    amount = State()

class SenderAdmin(StatesGroup):
    msg = State()

class GetUser(StatesGroup):
    user_id = State()

class ChangeBalance(StatesGroup):
    amount = State()