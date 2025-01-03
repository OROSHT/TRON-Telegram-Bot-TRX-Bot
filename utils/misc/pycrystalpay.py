from __future__ import annotations
import httpx
from json import loads

class CrystalPay:
    def __init__(self, auth_login: str, auth_secret: str) -> CrystalPay:
        self.cash_name = auth_login
        self.secret_1 = auth_secret
        self.api_url = "https://api.crystalpay.io/v2"
        self.def_params = {"auth_secret": self.secret_1, "auth_login": self.cash_name}
        self.headers = {"Content-Type": "application/json"}
        self.client = httpx.AsyncClient(headers=self.headers)
        
    async def get_cash_balance(self) -> list:
        params = self.def_params.copy()
        params['hide_empty'] = "false"
        data = await self.client.post(f"{self.api_url}/balance/info/", json=params).json()
        if data.get('error'):
            raise AuthError("Не удалось получить баланс кассы! Ошибка авторизации!")
        return data['balances']

    async def create_invoice(self, amount: int, lifetime: int = 60, type_: str = "purchase") -> dict:
        params = self.def_params.copy()
        params.update({"amount": amount, "lifetime": lifetime, "type": type_})
        data = await self.client.post(f"{self.api_url}/invoice/create/", json=params).json()
        if data.get('error'):
            raise AuthError("Не смог создать платеж! Ошибка авторизации!")
        return data

    async def if_paid(self, id: int) -> bool:
        params = self.def_params.copy()
        params['id'] = id
        data = await self.client.post(f"{self.api_url}/invoice/info/", json=params).json()
        if data.get('error'):
            raise AuthError("Не смог проверить оплату платежа! Ошибка авторизации!")
        return data['state'] == "payed"

class AuthError(Exception):
    pass
