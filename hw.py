import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from config import TOKEN, API_GIF
import requests
import logging
from keyboards import keyboard
from jokeapi import Jokes # Import the Jokes class
from googletrans import Translator  # Импортируем библиотеку для перевода

logging.basicConfig(level=logging.INFO)


bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()  # Создаем объект для перевода

# Обработчик команды /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Я бот, который может подбирать GIF по ключевому слову и выдавать произвольную шутку. "
                         "Выберите опцию", reply_markup=keyboard)


#  JokeAPI может возвращать шутки двух типов:
#    - `single`: шутка, состоящая из одного предложения. Шутка содержится в поле `joke`.
#    - `twopart`: шутка, состоящая из двух частей — зачин (setup) и развязка (delivery).
# blacklist=['nsfw', 'racist'])  - Will return a joke that does not have either the flag "nsfw" or "racist".
@dp.callback_query(F.data == 'random_joke')
async def random_joke(callback: CallbackQuery):
    j = await Jokes()  # Initialise the class
    joke = await j.get_joke(blacklist=['nsfw', 'racist'])
    if joke['type'] == 'single':
        translated_joke_no_text = await translator.translate(joke['joke'], dest='ru')
        translated_joke = translated_joke_no_text.text
    else:
        translated_setup = await translator.translate(joke['setup'], dest='ru')
        translated_delivery = await translator.translate(joke['delivery'], dest='ru')
        translated_joke = f"- {translated_setup.text}\n - {translated_delivery.text}"
    await callback.answer('Произвольная шутка подобрана!')
    await callback.message.answer(f'Шутка:\n {translated_joke}')


async def main():
    await dp.start_polling(bot)


asyncio.run(main())
