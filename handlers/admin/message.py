from aiogram import types
from aiogram.dispatcher import FSMContext
from filters.filters import IsAdmin
from loader import dp, db, bot, truncate
import keyboards.inline.keyboard as kb
import states.States as st

@dp.message_handler(IsAdmin(), commands=["admin"], state="*", chat_type=["private"])
async def admin_start(message: types.Message, state: FSMContext):
    await message.answer("📚 Админ панель", reply_markup=kb.admin_keyboard())

@dp.message_handler(IsAdmin(), state=st.SenderAdmin.msg, content_types=["any"])
async def senderadmin(message: types.Message, state: FSMContext):
    data = await state.get_data()
    msg = data["msg"]
    await msg.delete()
    await state.finish()
    await message.answer("⚠️ Начинаю рассылку!", reply_markup=kb.cancel_admin())
    users = await db.get_all_users()
    valid = nevalid = 0
    for x in users:
        try:
            await message.copy_to(chat_id=x[0])
            valid += 1
        except:
            nevalid += 1
    await message.answer(f"""<b>
🎉 Успешно закончил рассылку

✅ Успешно отправлено: <code>{valid}</code>
❌ Ошибок при отправке: <code>{nevalid}</code>
👥 Всего пользователей: <code>{len(users)}</code></b>""")

@dp.message_handler(IsAdmin(), state=st.GetUser.user_id, content_types=["text"])
async def get_user_info(message: types.Message, state: FSMContext):
    user = message.text
    data = await state.get_data()
    msg = data["msg"]
    await msg.delete()
    info = await db.get_user(user) if user.isdigit() else await db.get_username(user)
    if not info:
        msg = await message.answer("❗️ Такого пользователя не существует", reply_markup=kb.cancel_admin())
        await state.update_data(msg=msg)
        return
    await state.finish()
    status = {0: "❌", 1: "✅"}
    count = await db.get_count(info.user_id)
    await message.answer(f"""<b>
👤 Пользователь @{info.username} (<code>{info.user_id}</code>)

💸 Баланс пользователя: <code>{truncate(info.balance, 2)}</code>
📬 Адрес TRX: <code>{info.adress}</code>
♻️ Совершил обменов: <code>{count}</code>
📜 Согласился с правилами: {status[info.accept]}
</b>""", reply_markup=kb.find_user(info.user_id, info.banned))

@dp.message_handler(IsAdmin(), state=st.ChangeBalance.amount, content_types=["text"])
async def change_balance(message: types.Message, state: FSMContext):
    amount = message.text
    data = await state.get_data()
    msg = data["msg"]
    await msg.delete()
    if not amount.replace("-", "", 1).isdigit():
        msg = await message.answer("⚠️ Введите целое число!", reply_markup=kb.cancel_admin())
        await state.update_data(msg=msg)
        return
    amount = int(amount)
    if amount == 0:
        msg = await message.answer("❗️ Зачем пользователю изменять баланс на 0? Введите нормальное число!", reply_markup=kb.cancel_admin())
        await state.update_data(msg=msg)
        return
    await state.finish()
    user_id = data["user_id"]
    await db.change_balance(user_id=user_id, amount=amount)
    textt = "пополнил вам баланс на" if amount > 0 else "снял с вашего баланса"
    try:
        await bot.send_message(user_id, f"👨‍💻 Администратор {textt} {amount} руб")
    except:
        pass
    info = await db.get_user(user_id=user_id)
    status = {0: "❌", 1: "✅"}
    count = await db.get_count(info.user_id)
    await message.answer(f"""<b>
👤 Пользователь @{info.username} (<code>{info.user_id}</code>)

💸 Баланс пользователя: <code>{truncate(info.balance, 2)}</code>
📬 Адрес TRX: <code>{info.adress}</code>
♻️ Совершил обменов: <code>{count}</code>
📜 Согласился с правилами: {status[info.accept]}
</b>""", reply_markup=kb.find_user(info.user_id, info.banned))
