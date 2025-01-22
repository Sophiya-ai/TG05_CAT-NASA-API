import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from config import TOKEN, API_GIF, JOKE_API_URL
import requests
import logging
from keyboards import keyboard

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()


# `Any?lang=ru` - запрашиваем любую шутку (`Any`) на русском языке
#  JokeAPI может возвращать шутки двух типов:
#    - `single`: шутка, состоящая из одного предложения. Шутка содержится в поле `joke`.
#    - `twopart`: шутка, состоящая из двух частей — зачин (setup) и развязка (delivery).
def get_random_joke():
    response = requests.get(f"{JOKE_API_URL}Any?lang=ru")
    if response.status_code == 200:
        data = response.json()
        if data['type'] == 'single':
            return data['joke']
        else:
            return f"{data['setup']} - {data['delivery']}"
    return "Не удалось получить шутку."


# Обработчик команды /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Я бот, который может подбирать GIF по ключевому слову и выдавать произвольную шутку. "
                         "Выберите опцию", reply_markup=keyboard)


@dp.callback_query(F.data == 'random_joke')
async def random_joke(callback: CallbackQuery):
    joke = get_random_joke()
    await callback.answer('Произвольная шутка подобрана!')
    await callback.message.answer('Шутка:', joke, reply_markup=ReplyKeyboardRemove())


async def main():
    await dp.start_polling(bot)


asyncio.run(main())
