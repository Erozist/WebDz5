import sys
from datetime import datetime, timedelta
# from pprint import pprint as print

import aiohttp
import asyncio
import json

async def fetch_exchange_rates(date):
    url = f"https://api.privatbank.ua/p24api/exchange_rates?date={date}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()



async def get_currency_rates(days):
    rates = []
    today = datetime.today()
    for i in range(days):
        date = (today - timedelta(days=i+1)).strftime('%d.%m.%Y')
        data = await fetch_exchange_rates(date)
        json_data = json.loads(data)

        eur_rate = None
        usd_rate = None
        if "exchangeRate" in json_data:
            for rate in json_data["exchangeRate"]:
                if rate["currency"] == "EUR":
                    eur_rate = {
                        "sale": rate.get("saleRate"),
                        "purchase": rate.get("purchaseRate")
                    }
                elif rate["currency"] == "USD":
                    usd_rate = {
                        "sale": rate.get("saleRate"),
                        "purchase": rate.get("purchaseRate")
                    }
                if eur_rate is not None and usd_rate is not None:
                    break

        rates.append({
            date: {
                "EUR": eur_rate,
                "USD": usd_rate
            }
        })
    return rates



async def main(days):
    try:
        rates = await get_currency_rates(days)
        print(json.dumps(rates, indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <number of days>")
        sys.exit(1)

    days = int(sys.argv[1])
    if days > 10:
        print("Error: Maximum number of days allowed is 10.")
        sys.exit(1)

    asyncio.run(main(days))
