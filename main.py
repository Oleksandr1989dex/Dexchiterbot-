import os
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
