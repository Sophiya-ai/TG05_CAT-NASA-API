import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import random
from config import TOKEN_CW, API_CAT

bot = Bot(token=TOKEN_CW)
dp = Dispatcher()



async def main():
    await dp.start_polling(bot)

asyncio.run(main())