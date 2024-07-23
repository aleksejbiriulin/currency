import asyncio
import aiohttp
import xml.etree.ElementTree as ET

async def get_currency_rates():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://cbr.ru/scripts/XML_daily.asp") as response:
            xml_content = await response.text()

    root = ET.fromstring(xml_content)
    currencies = root.findall("Valute")

    for currency in currencies:
        currency_code = currency.find("CharCode").text
        currency_name = currency.find("Name").text
        currency_rate = float(currency.find("Value").text.replace(",", "."))

        print(f"Валюта: {currency_name} ({currency_code})")
        print(f"Курс: {currency_rate}")
        print()

async def main():
    await get_currency_rates()

if __name__ == "__main__":
    asyncio.run(main())
