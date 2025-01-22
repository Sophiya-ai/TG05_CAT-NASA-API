import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from config import TOKEN, API_GIF, JOKE_API_URL
import requests
import logging
from keyboards import keyboard

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()







async def main():
    await dp.start_polling(bot)


asyncio.run(main())