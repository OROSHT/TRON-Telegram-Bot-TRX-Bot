from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot, truncate
from filters.filters import IsAdmin
import keyboards.inline.keyboard as kb
import states.States as st

def get_fake_results(list_c: list[str], start_num: int, size: int = 50):
    overall_items = len(list_c)
    if start_num >= overall_items:
        return []
    elif start_num + size >= overall_items:
        return list_c[start_num:overall_items]
    else:
        return list_c[start_num:start_num + size]

@dp.callback_query_handler(IsAdmin(), text=["cancel_admin"], state="*")
async def cancel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer('📚 Админ панель', reply_markup=kb.admin_keyboard())

@dp.inline_handler(IsAdmin(), text="obmen")
async def test(query: types.InlineQuery, state: FSMContext):
    get_history = await db.get_history()
    query_offset = int(query.offset) if query.offset else 0
    if not get_history:
        await query.answer([], cache_time=5, is_personal=True, switch_pm_parameter="admin", switch_pm_text="В данный момент список обменов пуст!")
    articles = [types.InlineQueryResultArticle(
        id=value,
        title=f"Дата обмена {item[4]}",
        description=f"Пользователь {item[0]} | {item[3]} RUB —> {item[2]} TRX",
        hide_url=False,
        input_message_content=types.InputTextMessageContent(
            message_text=f"""
🗓 Дата обмена <code>{item[4]}</code>
👤 Пользователь: <code>{item[0]}</code>
📬 Кошелек получателя: <code>{item[1]}</code>
✅ <code>{item[3]}</code> RUB —> <code>{item[2]}</code> TRX
"""
        )
    ) for value, item in enumerate(get_fake_results(get_history, query_offset))]
    if len(articles) < 50:
        await query.answer(articles, is_personal=True, next_offset="", cache_time=5)
    else:
        await query.answer(articles, is_personal=True, next_offset=str(query_offset + 50), cache_time=5)

@dp.callback_query_handler(IsAdmin(), text="stats", state="*")
async def sss(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    a, b, c, d, e, f, g, h = await db.get_all_info()
    await call.message.answer(f"""<b>
~ Статистика бота @{(await bot.get_me()).username} ~

♻️ Всего обменов совершенно: <code>{a}</code>
📝 Оборот проекта в рублях: <code>{truncate(b, 2)}</code>
💸 Общий баланс бота: <code>{truncate(c, 2)}</code>
1️⃣ Пользователей за день: <code>{d}</code>
2️⃣ Пользователей за неделю: <code>{e}</code>
3️⃣ Пользователей за месяц: <code>{f}</code>
🛡 Забаненных пользователей: <code>{g}</code>
👥 Всего пользователей: <code>{h}</code>
</b>""", reply_markup=kb.cancel_admin())

@dp.callback_query_handler(IsAdmin(), text="sender", state="*")
async def sss1(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    msg = await call.message.answer("Отправьте сообщение для рассылки:", reply_markup=kb.cancel_admin())
    await state.update_data(msg=msg)
    await st.SenderAdmin.msg.set()

@dp.callback_query_handler(IsAdmin(), text="find_user", state="*")
async def sss2(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    msg = await call.message.answer("Отправьте ID или Username пользователя:", reply_markup=kb.cancel_admin())
    await state.update_data(msg=msg)
    await st.GetUser.user_id.set()

@dp.callback_query_handler(IsAdmin(), text_contains="banned|", state="*")
async def sss3(call: types.CallbackQuery, state: FSMContext):
    data, user_id, status = call.data.split("|")
    await call.message.delete()
    await db.update_banned(user_id=user_id, banned=status)
    info = await db.get_user(user_id=user_id)
    status = {0: "❌", 1: "✅"}
    count = await db.get_count(info.user_id)
    await call.message.answer(f"""<b>
👤 Пользователь @{info.username} (<code>{info.user_id}</code>)

💸 Баланс пользователя: <code>{truncate(info.balance, 2)}</code>
📬 Адрес TRX: <code>{info.adress}</code>
♻️ Совершил обменов: <code>{count}</code>
📜 Согласился с правилами: {status[info.accept]}
</b>""", reply_markup=kb.find_user(info.user_id, info.banned))

@dp.callback_query_handler(IsAdmin(), text_contains="chan_balance|", state="*")
async def sss4(call: types.CallbackQuery, state: FSMContext):
    user_id = call.data.split("|")[-1]
    await call.message.delete()
    msg = await call.message.answer("Введите сумму пополнения/снятия\nПример: -100 (чтобы забрать у пользователя 100р с баланса)", reply_markup=kb.cancel_admin())
    await state.update_data(msg=msg, user_id=user_id)
    await st.ChangeBalance.amount.set()
