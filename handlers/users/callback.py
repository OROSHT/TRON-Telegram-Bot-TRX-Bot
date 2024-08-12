from aiogram import types
from aiogram.dispatcher import FSMContext
import keyboards.inline.keyboard as kb_in
import states.States as stat
import loader
from loader import dp, db, bot, truncate
from data import config
from utils.misc.Trx import send_tron


@dp.callback_query_handler(text=["cancel", "cancel_n"], state="*")
async def cancel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    if call.data != "cancel_n":
        await call.message.delete()
    else:
        await call.message.edit_reply_markup(None)
    await call.message.answer(f'👋 Приветствую тебя, {call.from_user.first_name}', reply_markup=kb_in.start())


@dp.callback_query_handler(text=["change"], state="*")
async def show_course(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    pars_ = await db.get_course()
    kurs = truncate(pars_ + pars_ * config.kurs / 100)
    await call.message.answer(f"""
Курсы валют:

Tron (TRX) - {kurs} руб
Выберите валюту для покупки:""", reply_markup=kb_in.change_keyboard())


@dp.callback_query_handler(text=["buy_tron"], state="*")
async def request_trx_amount(call: types.CallbackQuery, state: FSMContext):
    info = await db.get_user(call.from_user.id)
    if not info.adress:
        await call.answer("❗️ Чтобы обменять TRX нужно указать адресс в «Профиле»", show_alert=True)
        return
    await call.message.delete()
    pars_ = await db.get_course()
    kurs = truncate(pars_ + pars_ * config.kurs / 100)
    msg = await call.message.answer(f"Отправьте сумму TRX, которую желаете приобрести\nКурс: {kurs} руб", reply_markup=kb_in.cancel())
    await state.update_data(msg=msg)
    await stat.GetTrx.amount.set()


@dp.callback_query_handler(text=["send_trx"], state="*")
async def process_trx_payment(call: types.CallbackQuery, state: FSMContext):
    msg = call.message.text.split("\n")
    adress = msg[2].split(": ")[-1]
    trx = int(msg[3].split(": ")[-1])
    rub = float(msg[4].split(": ")[-1])
    
    info = await db.get_user(call.from_user.id)
    if info.balance < rub:
        await call.answer("❗️ Недостаточно средств")
        return
    await call.message.delete()
    await db.change_balance(user_id=call.from_user.id, amount=-rub)
    
    status = await send_tron(wallet=adress, amount=trx)
    if status["status"]:
        await db.insert_history(user_id=call.from_user.id, adress=adress, TRX=trx, RUB=rub)
        await call.message.answer(f'✅ Успешно отправил {trx} TRX\n🔗 Транзакция: https://tronscan.org/#/transaction/{status["tx"]}', reply_markup=kb_in.cancel_n())
        await bot.send_message(chat_id=config.sender_id, text=f"@{call.from_user.username} ({call.from_user.id}) | {rub} RUB —> {trx} TRX")
    else:
        await db.change_balance(user_id=call.from_user.id, amount=rub)
        await call.message.answer(f'❌ Возникла ошибка при выводе\n⚠️ Сообщение отправлено администратору!', reply_markup=kb_in.cancel_n())
        await bot.send_message(chat_id=config.sender_id, text=f"""
<b>❌ Ошибка при отправке TRX

Telegram ID: <code>{call.from_user.id}</code>
Telegram Username: <code>{call.from_user.username}</code>
Баланс пользователя: <code>{info.balance}</code>
Кошелек пользователя: <code>{info.adress}</code>
Сумма вывода: <code>{trx}</code>
Ошибка: <code>{str(status['error'])}</code>
</b>""")


@dp.callback_query_handler(text=["information"], state="*")
async def show_information(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("ℹ️ Информация о нас", reply_markup=kb_in.create_information(config.links))


@dp.callback_query_handler(text=["profile"], state="*")
async def show_profile(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    info = await db.get_user(call.from_user.id)
    count = await db.get_count(call.from_user.id)
    await call.message.answer(f"""<b>
💎 Личный кабинет:

🆔 ID: <code>{call.from_user.id}</code>
⚡️ Username: <code>{call.from_user.username}</code>
💸 Баланс: <code>{truncate(info.balance, 2)}</code> руб
♻️ Количество сделок: <code>{count}</code>
📫 Адрес TRX: <code>{info.adress}</code></b>""", reply_markup=kb_in.profile())


@dp.callback_query_handler(text=["change_adres"], state="*")
async def request_new_address(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    msg = await call.message.answer("⚠️ Введите новый адрес TRX кошелька:", reply_markup=kb_in.cancel())
    await state.update_data(msg=msg)
    await stat.ChangeTrx.adres.set()


@dp.callback_query_handler(text=["up_balance"], state="*")
async def choose_payment_system(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Выберите платёжную систему:", reply_markup=kb_in.choice_up(config.platega))


@dp.callback_query_handler(text_contains=["payment_generate|"], state="*")
async def generate_payment(call: types.CallbackQuery, state: FSMContext):
    payment = call.data.split("|")[-1]
    await state.update_data(payment=payment)
    await call.message.delete()
    msg = await call.message.answer("Введите сумму пополнения:", reply_markup=kb_in.cancel())
    await state.update_data(msg=msg)
    await stat.UpdateBalance.amount.set()


@dp.callback_query_handler(text=["reject_qiwi"], state="*")
async def reject_qiwi_payment(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    bill_id = call.message.text.split("\n")[-1].replace("🆔 ID платежа: ", "")
    await loader.client_qiwi.reject_p2p_bill(bill_id=bill_id)
    await call.message.delete()
    await call.message.answer(f'👋 Приветствую тебя, {call.from_user.first_name}', reply_markup=kb_in.start())


@dp.callback_query_handler(text=["check_pay|QIWI"], state="*")
async def check_qiwi_payment(call: types.CallbackQuery, state: FSMContext):
    msg = call.message.text.split("\n")
    amount = int(msg[1].replace("💸 Сумма к оплате: ", "").replace(" rub", ""))
    bill_id = msg[2].replace("🆔 ID платежа: ", "")
    status = await loader.client_qiwi.get_bill_status(bill_id=bill_id)
    if status == "PAID":
        await call.message.delete()
        await call.answer("✅ Платёж найден!")
        await call.message.answer("Платёж найден", reply_markup=kb_in.start())
        await db.change_balance(call.from_user.id, amount)
        await bot.send_message(chat_id=config.sender_id, text=f"✅ Пополнение баланса @{call.from_user.username} ({call.from_user.id}) | QIWI | +{amount} rub")
    else:
        await call.answer("⚠️ Платёж не найден")


@dp.callback_query_handler(text=["check_pay|CrystalPay"], state="*")
async def check_crystalpay_payment(call: types.CallbackQuery, state: FSMContext):
    msg = call.message.text.split("\n")
    amount = int(msg[1].replace("💸 Сумма к оплате: ", "").replace(" rub", ""))
    bill_id = msg[2].replace("🆔 ID платежа: ", "")
    status = await loader.client_cry.if_paid(id=bill_id)
    if status:
        await call.message.delete()
        await call.answer("✅ Платёж найден!")
        await call.message.answer("Платёж найден", reply_markup=kb_in.start())
        await db.change_balance(call.from_user.id, amount)
        await bot.send_message(chat_id=config.sender_id, text=f"✅ Пополнение баланса @{call.from_user.username} ({call.from_user.id}) | CrystalPay | +{amount} rub")
    else:
        await call.answer("⚠️ Платёж не найден")


@dp.callback_query_handler(text=["check_pay|YooMoney"], state="*")
async def check_yoomoney_payment(call: types.CallbackQuery, state: FSMContext):
    msg = call.message.text.split("\n")
    amount = float(msg[1].replace("💸 Сумма к оплате: ", "").replace(" rub", ""))
    bill_id = msg[2].replace("🆔 ID платежа: ", "")
    payments = (await loader.client_ym.operation_history(label=bill_id, records=5)).operations[:5]
    for payment in payments:
        if payment.label == bill_id:
            amount = payment.amount
            await call.message.delete()
            await call.answer("✅ Платёж найден!")
            await call.message.answer("Платёж найден", reply_markup=kb_in.start())
            await db.change_balance(call.from_user.id, amount)
            await bot.send_message(chat_id=config.sender_id, text=f"✅ Пополнение баланса @{call.from_user.username} ({call.from_user.id}) | YooMoney | +{amount} rub")
            break
    else:
        await call.answer("⚠️ Платёж не найден")


@dp.callback_query_handler(text=["accept_rules"], state="*")
async def accept_rules(call: types.CallbackQuery, state: FSMContext):
    await db.change_accept(call.from_user.id)
    await call.message.delete()
    await call.message.answer(f'👋 Приветствую тебя, {call.from_user.first_name}', reply_markup=kb_in.start())


@dp.callback_query_handler(text=["check_rules"], state="*")
async def check_rules(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("<b>"+config.rules+"</b>", reply_markup=kb_in.cancel())
