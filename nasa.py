import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import random
from datetime import datetime, timedelta
from config import TOKEN_CW, API_NASA_KEY
import requests

bot = Bot(token=TOKEN_CW)
dp = Dispatcher()


# - apod - astronomic picture of the day
# - Указываем начальную дату — за год до конечной даты random.random выдаёт случайное число от 0 до 1.
#   365 дней умножаются на дробное число, получается некое количество дней.
#   Это количество дней прибавляется к начальной дате. Полученный день сохраняется в переменную random_date
# - Из документации берём ссылку и работаем с ней. Создаём переменную url внутри функции.
#   Через эту переменную мы будем отправлять GET-запрос. Добавляем учёт и API-ключа, и даты (через &)
def get_random_apod():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    random_date = start_date + (end_date - start_date) * random.random()
    date_str = random_date.strftime('%Y-%m-%d')

    url = f'https://api.nasa.gov/planetary/apod?api_key={API_NASA_KEY}&date={date_str}'
    response = requests.get(url)
    return response.json()


@dp.message(Command('random_apod'))
async def random_apod(message: Message):
    apod = get_random_apod()
    photo_url = apod['url']
    title = apod['title']
    description = apod['explanation']

    await message.answer_photo(photo=photo_url, caption=f'{title}\n \n {description}')


async def main():
    await dp.start_polling(bot)


asyncio.run(main())
