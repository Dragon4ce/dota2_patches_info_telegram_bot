import asyncio
import os
import logging
from dotenv import load_dotenv

from aiohttp import *
from aiogram.filters import CommandStart
from aiogram import Dispatcher, Bot
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(level=logging.INFO)

if not TOKEN:
    raise ValueError('Нет токена')

dp = Dispatcher()
bot = Bot(token=TOKEN)


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Введите имя героя')


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print('Бот запущен')
    await dp.start_polling(bot)


if name == 'main':
    asyncio.run(main())