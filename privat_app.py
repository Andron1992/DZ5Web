import aiohttp
import asyncio
from utils import handle_errors


class PrivatBankAPI:
    BASE_URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date="

    async def get_exchange_rates(self, date: str):
        url = f"{self.BASE_URL}{date}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    response.raise_for_status()
                    date = await response.json()
                    return self.parse_exchange_rates(date)
            except Exception as e:
                handle_errors(e, date)
                return None

    def parse_exchange_rates(self, data):
        date = data.get("date")
        exchange_rates = data.get("exchangeRate", [])

        rates = {"EUR": {}, "USD": {}}
        for rate in exchange_rates:
            if rate.get("currency") in rates:
                rates[rate["currency"]] = {"sale": rate.get("saleRate"), "purchase": rate.get("purchaseRate")}
        return  {date: rates}