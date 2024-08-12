from aiogram import types
from aiogram.dispatcher import FSMContext
import keyboards.inline.keyboard as kb_in
from loader import dp, db, bot, truncate
import loader
import states.States as stat
from data import config
from utils.misc.Trx import get_balance
import time



@dp.message_handler(commands=["start"], state="*", chat_type=["private"])
async def bot_echo_all(message: types.Message, state: FSMContext):
    await state.finish()
    await db.add_db(message.from_user.id, message.from_user.username)

    get_info = await db.get_user(message.from_user.id)
    if get_info.accept == 0:
        await message.answer("<b>"+config.rules+"</b>", reply_markup=kb_in.accept_rules())
        return
    

    await message.answer(f'👋 Приветствую тебя, {message.from_user.first_name}', reply_markup=kb_in.start())


@dp.message_handler(state=stat.GetTrx.amount)
async def ss3(message: types.Message, state: FSMContext):
    try:
        amount = message.text
        data = await state.get_data()
        msg = data["msg"]
        await msg.delete()
        try:
            amount = int(amount)
            if amount <= 0:
                msg = await message.answer("❌ Введите число больше нуля! (Целое число)", reply_markup=kb_in.cancel())
                await state.update_data(msg=msg)
                return
        except:
            msg = await message.answer("❌ Пожалуйста, введите число! (Целое число)", reply_markup=kb_in.cancel())
            await state.update_data(msg=msg)
            return

        if amount < config.min_buy:
            msg = await message.answer(f"❗️ Минимальное количество TRX для покупки — {config.min_buy}", reply_markup=kb_in.cancel())
            await state.update_data(msg=msg)
            return

        all_bank = await get_balance(config.adress)
        
        if not all_bank['status']:
            await message.answer("❗️ Возникла неизвестная ошибка\n⚠️ Попробуйте чуть позже!", reply_markup=kb_in.cancel_n())
            await state.finish()
            return

        all_bank = int(float(all_bank["balance"]))
        if all_bank < float(amount):
            msg = await message.answer(f"❗️ Недостаточно средств на кошельке\n⚠️ Доступно: {all_bank} TRX", reply_markup=kb_in.cancel())
            await state.update_data(msg=msg)
            return

        pars_ = await db.get_course()
        kurs =  pars_ + pars_ * config.kurs / 100
        summa = truncate(kurs * amount, 2)
        information = await db.get_user(message.from_user.id)

        if information.balance < summa:
            msg = await message.answer(f"❗️ Недостаточно средств, пополните баланс в профиле\n💸 Сумма к оплате: {summa}\n💰 Ваш баланс: {truncate(information.balance, 2)}", reply_markup=kb_in.cancel())
            await state.update_data(msg=msg)
            return
        
        await state.finish()
        await message.answer(f"""
<b>⚠️ Проверьте правильность данных!

📫 Адрес TRX: <code>{information.adress}</code>
📤 Вы получите TRX: <code>{amount}</code>
📥 Вы заплатите RUB: <code>{summa}</code></b>""", reply_markup=kb_in.successful())
    except:
        pass





@dp.message_handler(state=stat.ChangeTrx.adres)
async def ss3(message: types.Message, state: FSMContext):
    adres = message.text
    
    data = await state.get_data()
    msg = data['msg']
    await msg.delete()

    if len(adres) != 34:
        msg = await message.answer("⚠️ Пожалуйста, введите верный кошелек:", reply_markup=kb_in.cancel())
        await state.update_data(msg=msg)
        return
    await state.finish()
    await db.change_adres(user_id=message.from_user.id, adress=adres)

    info = await db.get_user(message.from_user.id)
    count = await db.get_count(message.from_user.id)
    await message.answer(f"""<b>
💎 Личный кабинет:

🆔 ID: <code>{message.from_user.id}</code>
⚡️ Username: <code>{message.from_user.username}</code>
💸 Баланс: <code>{truncate(info.balance, 2)}</code> руб
♻️ Количество сделок: <code>{count}</code>
📫 Адрес TRX: <code>{info.adress}</code></b>""", reply_markup=kb_in.profile())


@dp.message_handler(state=stat.UpdateBalance.amount)
async def ss13(message: types.Message, state: FSMContext):
    amount = message.text
    data = await state.get_data()
    msg = data["msg"]
    await msg.delete()


    if not amount.isdigit():
        msg = await message.answer("❗️ Пожалуйста, введите целое число!", reply_markup=kb_in.cancel())
        await state.update_data(msg=msg)
        return
    
    amount = int(amount)
    if amount <= 0:
        msg = await message.answer("❗️ Число должно быть больше нуля!", reply_markup=kb_in.cancel())
        await state.update_data(msg=msg)
        return
    
    if amount < config.min_upgrade:
        msg = await message.answer(f"❗️ Минимальная сумма для пополнения составляет {config.min_upgrade} рублей!", reply_markup=kb_in.cancel())
        await state.update_data(msg=msg)
        return

    payment = data["payment"]
    await state.finish()

    if payment == "QIWI":

        result = await loader.client_qiwi.create_p2p_bill(amount=amount)

        bill_id, pay_url = result.id, result.pay_url

    elif payment == "YooMoney":

        amount += truncate(amount*3/100, 2)

        account = (await loader.client_ym.retrieve_account_info()).account
        bill_id = f"{message.from_user.id}_{int(time.time())}"
        pay_url = loader.client_ym.create_pay_form(
                                                receiver=account,
                                                quick_pay_form="shop",
                                                targets="Balance",
                                                payment_type="PC",
                                                amount=amount,
                                                label=bill_id)
    elif payment == "CrystalPay":
        result = await loader.client_cry.create_invoice(amount=amount)

        bill_id, pay_url = result["id"], result["url"]
            

    await message.answer(f"""
💳 Метод пополнения: <code>{payment}</code>
💸 Сумма к оплате: <code>{amount}</code> rub
🆔 ID платежа: <code>{bill_id}</code>""", reply_markup=kb_in.keyboard_payment(payment=payment, url=pay_url))