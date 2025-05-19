import asyncio
import logging
import aiohttp
from aiogram import Bot, Dispatcher, types

API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def fetch_data():
    url = 'https://api.dexscreener.com/latest/dex/pairs'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def check_tokens():
    while True:
        try:
            data = await fetch_data()
            # Фільтрація за критеріями: біржа MEXC, відсутність на Binance, різниця цін > 7%
            # Тут має бути ваша логіка
            # Якщо є відповідність — надсилаємо повідомлення
            await bot.send_message(chat_id='YOUR_CHAT_ID', text='Token meets criteria.')
        except Exception as e:
            logging.error(f'Error fetching data: {e}')
        await asyncio.sleep(60)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Бот працює. Щохвилини перевіряє токени.")

async def main():
    asyncio.create_task(check_tokens())
    await dp.start_polling()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
