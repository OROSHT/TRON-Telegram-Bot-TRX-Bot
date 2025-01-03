from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data import config
from utils.db_api.db_file import DataBase
from glQiwiApi import YooMoneyAPI, QiwiP2PClient
from utils.misc.pycrystalpay import CrystalPay

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = DataBase("db.db")

if config.platega["🥝 QIWI"]["key"]:
    client_qiwi = QiwiP2PClient(secret_p2p=config.platega["🥝 QIWI"]["key"])

if config.platega["🟣 YooMoney"]["key"]:
    client_ym = YooMoneyAPI(api_access_token=config.platega["🟣 YooMoney"]["key"])

if config.platega["💎 CrystalPay"]["key"]:
    client_cry = CrystalPay(
        auth_secret=config.platega["💎 CrystalPay"]["key"],
        auth_login=config.platega["💎 CrystalPay"]["login"]
    )

def truncate(n, c=2):
    return int(n * (10 ** c)) / (10 ** c)
