import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import random
from config import TOKEN_CW, API_CAT_KEY
import requests

bot = Bot(token=TOKEN_CW)
dp = Dispatcher()


# To get more than 10, and additional fields then be sure to use your API Key
# from the welcome email as the 'x-api-key' header
def get_cat_breeds():
    url = 'https://api.thecatapi.com/v1/breeds'
    headers = {'x-api-key': API_CAT_KEY}
    response = requests.get(url, headers=headers)
    return response.json()


def get_cat_image_by_breed(breed_id):
    url = f'https://api.thecatapi.com/v1/images/search?breed_ids={breed_id}'
    headers = {'x-api-key': API_CAT_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data[0]['url']


def get_breed_info(breed_name):
    breeds = get_cat_breeds()
    for breed in breeds:
        if breed['name'].lower() == breed_name.lower():
            return breed
    return None


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет! Напиши мне название породы кошки, '
                         'и я пришлю ее фото и информацию ней.')


@dp.message()
async def send_cat_info(message: Message):
    breed_name = message.text
    breed_info = get_breed_info(breed_name)
    if breed_info:
        cat_img_url = get_cat_image_by_breed(breed_info['id'])
        info = (f'Порода - {breed_info['name']}\n'
                f'Описание - {breed_info['description']}\n'
                f'Продолжительность жизни - {breed_info['life_span']}\n')
        await message.answer_photo(photo=cat_img_url, caption=info)
    else:
        await message.answer('Порода не найдена')


async def main():
    await dp.start_polling(bot)


asyncio.run(main())
