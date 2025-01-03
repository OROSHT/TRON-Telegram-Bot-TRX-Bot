from tronpy import Tron
from tronpy.providers import HTTPProvider
from tronpy.keys import PrivateKey
from data import config
import httpx
import re

client = Tron(HTTPProvider(api_key=config.api_keys), network='nile')
priv_key = PrivateKey(bytes.fromhex(config.private_key))

async def get_balance(wallet: str) -> dict:
    try:
        async with httpx.AsyncClient() as http_client:
            response = await http_client.get(f"https://apilist.tronscan.org/api/account?address={wallet}")
            balance = response.json()["balances"][0]["amount"]
            return {"status": True, "balance": balance}
    except Exception as ex:
        return {"status": False, "error": str(ex)}

async def send_tron(wallet: str, amount: int) -> dict:
    try:
        txn = (
            client.trx.transfer(config.adress, wallet, amount * 1_000_000)
            .memo("Transaction")
            .build()
            .inspect()
            .sign(priv_key)
            .broadcast()
        )
        return {"status": True, "tx": txn.txid}
    except Exception as ex:
        return {"status": False, "error": str(ex)}

async def get_course() -> float:
    async with httpx.AsyncClient() as http_client:
        response = await http_client.get('https://ru.investing.com/crypto/tron/trx-rub')
        result = float(re.findall('instrument-price-last">(.*?)<', response.text)[0].replace(",", "."))
        return result
