import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from config import TOKEN, API_GIF
import requests
import logging
from keyboards import keyboard
from jokeapi import Jokes # Import the Jokes class

logging.basicConfig(level=logging.INFO)


bot = Bot(token=TOKEN)
dp = Dispatcher()







# Обработчик команды /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Я бот, который может подбирать GIF по ключевому слову и выдавать произвольную шутку. "
                         "Выберите опцию", reply_markup=keyboard)


#  JokeAPI может возвращать шутки двух типов:
#    - `single`: шутка, состоящая из одного предложения. Шутка содержится в поле `joke`.
#    - `twopart`: шутка, состоящая из двух частей — зачин (setup) и развязка (delivery).
@dp.callback_query(F.data == 'random_joke')
async def random_joke(callback: CallbackQuery):
    j = await Jokes()  # Initialise the class
    joke = await j.get_joke()  # Retrieve a random joke
    if joke['type'] == 'single':
        r_joke = joke['joke']
    else:
        r_joke = f"{joke['setup']} - {joke['delivery']}"
    await callback.answer('Произвольная шутка подобрана!')
    await callback.message.answer('Шутка:', r_joke)


async def main():
    await dp.start_polling(bot)


asyncio.run(main())
