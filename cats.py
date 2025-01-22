import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import random
from config import TOKEN_CW, API_CAT
import requests

bot = Bot(token=TOKEN_CW)
dp = Dispatcher()

def get_cat_breeds():
    url = 'https://api.thecatapi.com/v1/images/search?breed_ids=%7Bbreed.id%7D'
    headers = {'x-api-key' : API_CAT}
    response = requests.get(url, headers=headers)
    return response.json()

def get_cat_image_by_breed(breed_id):


async def main():
    await dp.start_polling(bot)

asyncio.run(main())