from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def start() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text="🔁 Обменять", callback_data="change"),
        InlineKeyboardButton(text="☃️ Профиль", callback_data="profile"),
        InlineKeyboardButton(text="🔰 О нас", callback_data="information"),
        InlineKeyboardButton(text="📜 Соглашение", callback_data="check_rules")
    ]
    keyboard.add(buttons[0])
    keyboard.add(buttons[1], buttons[2])
    keyboard.add(buttons[3])
    return keyboard

def change_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text="Tron (TRX)", callback_data="buy_tron"),
        InlineKeyboardButton(text="Закрыть", callback_data="cancel")
    ]
    keyboard.add(buttons[0])
    keyboard.add(buttons[1])
    return keyboard

def cancel() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(InlineKeyboardButton(text="Закрыть", callback_data="cancel"))
    return keyboard

def successful() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(InlineKeyboardButton(text="✅ Отправить", callback_data="send_trx"))
    return keyboard

def cancel_n() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(InlineKeyboardButton(text="Закрыть", callback_data="cancel_n"))
    return keyboard

def create_information(link: dict) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    for text, url in link.items():
        keyboard.add(InlineKeyboardButton(text=text, url=url))
    keyboard.add(InlineKeyboardButton(text="Закрыть", callback_data="cancel"))
    return keyboard

def profile() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text="💸 Пополнить баланс", callback_data="up_balance"),
        InlineKeyboardButton(text="⚙️ Изменить адрес", callback_data="change_adres"),
        InlineKeyboardButton(text="Закрыть", callback_data="cancel")
    ]
    keyboard.add(buttons[0])
    keyboard.add(buttons[1])
    keyboard.add(buttons[2])
    return keyboard

def admin_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text="📊 Статистика", callback_data="stats"),
        InlineKeyboardButton(text="📣 Рассылка", callback_data="sender"),
        InlineKeyboardButton(text="🔍 Найти пользователя", callback_data="find_user"),
        InlineKeyboardButton(text="📃 История обменов", switch_inline_query_current_chat="obmen")
    ]
    keyboard.add(buttons[2])
    keyboard.add(buttons[0], buttons[1])
    keyboard.add(buttons[3])
    return keyboard

def accept_rules() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(InlineKeyboardButton(text="✅ Принимаю правила", callback_data="accept_rules"))
    return keyboard

def find_user(user_id: int, banned: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    status_text = {0: "❌ Заблокировать", 1: "✅ Разблокировать"}
    status_value = {0: 1, 1: 0}
    buttons = [
        InlineKeyboardButton(text=status_text[banned], callback_data=f"banned|{user_id}|{status_value[banned]}"),
        InlineKeyboardButton(text="💰 Изменить баланс", callback_data=f"chan_balance|{user_id}"),
        InlineKeyboardButton(text="Закрыть", callback_data="cancel_admin")
    ]
    keyboard.add(buttons[0])
    keyboard.add(buttons[1])
    keyboard.add(buttons[2])
    return keyboard

def cancel_admin() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(InlineKeyboardButton(text="Закрыть", callback_data="cancel_admin"))
    return keyboard

def choice_up(platega_: dict) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text=payment, callback_data=f"payment_generate|{payment.split(' ')[-1]}")
        for payment in platega_ if platega_[payment]["key"]
    ]
    keyboard.add(*buttons)
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="cancel"))
    return keyboard

def keyboard_payment(payment: str, url: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(InlineKeyboardButton(text="🔗 Ссылка на оплату", url=url))
    keyboard.add(InlineKeyboardButton(text="✅ Оплатил", callback_data=f"check_pay|{payment}"))
    if payment == "QIWI":
        keyboard.add(InlineKeyboardButton(text="❌ Отмена", callback_data="reject_qiwi"))
    else:
        keyboard.add(InlineKeyboardButton(text="❌ Отмена", callback_data="cancel"))
    return keyboard
