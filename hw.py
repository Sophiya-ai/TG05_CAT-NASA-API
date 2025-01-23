import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from config import TOKEN, API_GIF
import requests
import logging
from keyboards import keyboard
from jokeapi import Jokes  # Import the Jokes class
from googletrans import Translator  # Импортируем библиотеку для перевода


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()  # Создаем объект для перевода


# Функция для поиска GIF по ключевым словам
def search_gif(search_term):
    url = f"https://tenor.googleapis.com/v2/search?q={search_term}&key={API_GIF}&limit=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['results'][0]['media_formats']['gif']['url'] #вывела json в консоль и нашла путь к url
    return None


# Обработчик команды /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Я бот, который может подбирать GIF по ключевому слову и выдавать произвольную шутку. "
                         "Выберите опцию", reply_markup=keyboard)


#  ---- Обработка кнопки - Случайная шутка ----
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


#  ---- Обработка кнопки - Популярный GIF ----
# Ввод запроса
@dp.callback_query(F.data == 'gif')
async def gif(callback: CallbackQuery):
    await callback.answer('Ключевое слово введено')
    await callback.message.answer('Введите ключевое слово для поиска GIF')


# Поиск по запросу (реагирует на любое введенное сообщение)
@dp.message()
async def text_message_handler(message: Message):
    search_term = message.text
    search_term_en = await translator.translate(search_term.lower(), dest='en')
    gif_url = search_gif(search_term_en)

    # try:
    #     # Check if the URL is a direct link to a GIF
    #     response = requests.head(gif_url)
    #     content_type = response.headers.get('Content-Type')
    #
    #     if content_type == 'image/gif':
    #         # Send the GIF
    #         await message.answer_animation(animation=gif_url, caption='Лучшая гифка в соответствии с вашим запросом')
    #     else:
    #         await message.reply("The provided URL does not point to a valid GIF file.")
    #
    # except Exception as e:
    #     await message.reply(f"An error occurred: {str(e)}")

    if gif_url:
        await message.answer_animation(animation=gif_url, caption='Лучшая гифка в соответствии с вашим запросом')
    else:
        await message.answer("Не удалось найти GIF по вашему запросу.")


async def main():
    await dp.start_polling(bot)


asyncio.run(main())
