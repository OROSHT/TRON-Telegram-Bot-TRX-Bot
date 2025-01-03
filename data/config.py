# ~~~~~~~~~~~~~~~~~~~~~~~~ Config ~~~~~~~~~~~~~~~~~~~~~~~~
BOT_TOKEN = "6218109657:AAHyONXg9o-SsNjt7yj1jMgqmin3mDSZVUM"
sender_id = 1
ADMINS = [941279996]
private_key = "2d23e6740ed6e381511c789fa67eeec4105d4f02484c7cfe0578ec4a07145dca"
adress = "TDUP6GAvJBhbxPFnYE3fkoTNMRcGCfMLNX"
api_keys = ["6076730d-1aea-4438-9aed-f2e5b9892982"]
kurs = 25
rate = 5
min_buy = 10
links = {
    "👨‍💻 Администратор": "https://t.me/waldau_admin",
    "🔗 Наша тема": "https://zelenka.guru/threads/5088116/",
    "Правила": "https://telegra.ph/Pravila-03-07-27"

}

platega = {
    "🥝 QIWI": {"key": ""},
    "🟣 YooMoney": {"key": "4100117975954375.ECE47FCB6C5E0DDEC69BF26CA7A5C8EE479FEC543C5039EAE5B806836D133A0644D201D813E7F683C97C7E48639C37EB31001FC4136195865785D96F5ADC4C0589595E625D384170C7839A6E45A484720F584362115ABC8B4290C721B60F7B6BF477DCDF757144BFC3CEC507B9721B761D52E98916669CC55B2B953A01482577"},
    "💎 CrystalPay": {"key": "aefa1235a6402fc320153538dd47a5bd67f51812", "login": "mgafina"}
}
min_upgrade = 1
rules = """
1. the exchanger works in automatic mode, without operators' participation.
2. The minimum exchange amount is 1 ruble, the maximum is 1,000,000 rubles. To exchange larger amounts, please contact an operator.
3. The exchange rate is calculated based on the current market value of cryptocurrency and may change online.
4. Before making an exchange, it is necessary to familiarize yourself with the terms of exchange, including the amount of commission that will be withheld during the exchange.
5. Exchange is performed only between RUB and TRX.
6. To make an exchange, you need to create an application on the exchanger's website, specifying the necessary data, such as the wallet number from which to send and to which to receive cryptocurrency.
7. After creating the application, it is necessary to make payment within the specified time, otherwise the application will be canceled.
8. The exchange is made within 2-3 minutes after payment is received.
9. The Exchanger is not responsible for erroneously specified data when creating an application, as well as for delays associated with the work of payment systems.
10. The Exchanger reserves the right to refuse the exchange without explaining the reasons."""
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
BOT_TOKEN - bot token | You can get it here https://t.me/BotFather.
ADMINS - List of admin IDs (Telegram IDs) | Get it here https://t.me/getmyid_bot.
private_key - Private key from your TronLink Pro wallet (see instructions on how to get it).
adress - The address of your TronLink Pro TRX (your Trx address).
api_keys - Api key(s) from https://www.trongrid.io/dashboard.
min_buy - Minimum number of TRX to buy.
links - Links to projects / admins, etc., whatever you want to specify, you don't have to have 3 like me, you can have 1 and 2 and 3 and 4....
platega - payment system setting, if you leave key: "" (empty), the payment system will be turned off!
min_upgrade - minimum replenishment amount
rules - rules
kurs - % markup for TRX sale, parses the rate from https://ru.investing.com/crypto/tron/trx-rub + your markup.
rate - (minutes) frequency with which the rate is updated in the bot, the rate is taken from https://ru.investing.com/crypto/tron/trx-rub.
"""
