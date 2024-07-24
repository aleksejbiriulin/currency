import asyncio
import aiohttp
import xml.etree.ElementTree as ET
import redis
from aiogram import Bot, Dispatcher, types
# from aiogram.utils import executor
from aiogram.filters import Command
from config import *

# Подключение к Redis
redis_client = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT))

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher() 


# Функция для получения курсов валют из XML
async def fetch_currency_rates():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://cbr.ru/scripts/XML_daily.asp") as response:
            xml_content = await response.text()

    root = ET.fromstring(xml_content)
    currencies = root.findall("Valute")

    for currency in currencies:
        currency_code = currency.find("CharCode").text
        currency_rate = float(currency.find("Value").text.replace(",", "."))
        redis_client.set(f"currency:{currency_code}", currency_rate)
    print(7)

# Функция для обработки команды /exchange
@dp.message(Command('/exchange'))
async def exchange_command(message: types.Message):
    try:
        _, from_currency, to_currency, amount = message.text.split()
        from_rate = float(redis_client.get(f"currency:{from_currency}"))
        to_rate = float(redis_client.get(f"currency:{to_currency}"))
        result = float(amount) * (to_rate / from_rate)
        await message.reply(f"{amount} {from_currency} = {result:.2f} {to_currency}")
    except (ValueError, IndexError):
        await message.reply("Неправильный формат команды. Пример: /exchange USD RUB 10")

# Функция для обработки команды /rates
@dp.message(Command('/rates'))
async def rates_command(message: types.Message):
    print(5)
    rates = ""
    for key in redis_client.keys("currency:*"):
        currency_code = key.decode().split(":")[1]
        currency_rate = float(redis_client.get(key))
        rates += f"{currency_code}: {currency_rate:.4f}\n"
    await message.reply(f"Актуальные курсы валют:\n{rates}")

    
async def main() -> None:
    print(5)
    asyncio.create_task(fetch_currency_rates())
    print(6)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
