main.py

import os
import asyncio
import logging
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.utils.exceptions import TelegramAPIError

# Читання змінних середовища
API_TOKEN = os.getenv("API_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # Наприклад: -1001234567890
INTERVAL = int(os.getenv("INTERVAL", 60))  # Інтервал у секундах, за замовчуванням 60

if not API_TOKEN or not CHANNEL_ID:
    raise ValueError("API_TOKEN або CHANNEL_ID не задано!")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

async def fetch_data():
    url = "https://api.dexscreener.com/latest/dex/pairs/mexc"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

def is_token_valid(token_data):
    try:
        price_mexc = float(token_data["priceUsd"])
        price_dex = float(token_data["dexIdPrice"])  # заміни на правильне поле, якщо інше
        price_diff = abs(price_mexc - price_dex) / price_dex * 100
        return price_diff >= 7
    except:
        return False

async def monitor_tokens():
    while True:
        try:
            data = await fetch_data()
            tokens = data.get("pairs", [])
            for token in tokens:
                if is_token_valid(token):
                    name = token.get("baseToken", {}).get("name")
                    symbol = token.get("baseToken", {}).get("symbol")
                    price = token.get("priceUsd")
                    url = token.get("url", "https://dexscreener.com/")
                    message = (
                        f"Знайдено токен:\n"
                        f"Назва: {name}\n"
                        f"Символ: {symbol}\n"
                        f"Ціна: ${price}\n"
                        f"{url}"
                    )
                    try:
                        await bot.send_message(chat_id=CHANNEL_ID, text=message)
                    except TelegramAPIError as e:
                        logging.error(f"Помилка надсилання повідомлення: {e}")
        except Exception as e:
            logging.error(f"Помилка при моніторингу токенів: {e}")
        await asyncio.sleep(INTERVAL)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(monitor_tokens())
    loop.run_forever()import os
import asyncio
from aiogram import Bot, Dispatcher, types

API_TOKEN = os.getenv("API_TOKEN")

if not API_TOKEN:
    raise ValueError("API_TOKEN is missing. Make sure it's set in the environment variables.")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.reply("Бот працює!")

async def main():
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
