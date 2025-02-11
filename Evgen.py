import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.types import Message
# from aiogram import executor  # Исправленный импорт
import aiohttp
import asyncio
import logging

# Токен вашего бота
TOKEN = "7868972083:AAHjnClkScE-lIJvTrzR3quHuiyXpPgy2nc"
# Ваш API-ключ от Unsplash
UNSPLASH_ACCESS_KEY = "EBGoYBeRzEXBPigGAlSBi1Lc8xsxerPt07WJ-sZBEMU"

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)


# Функция для получения координат города
async def get_coordinates(city_name):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city_name,
        "format": "json",
        "limit": 1,
        "accept-language": "ru"  # Указываем язык ответа
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=5) as response:
                data = await response.json()
                if data and len(data) > 0:
                    lat, lon = data[0]["lat"], data[0]["lon"]
                    return lat, lon
    except Exception as e:
        print(f"Ошибка получения координат: {e}")
        return None, None


# Функция для получения погоды
async def get_weather(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=5) as response:
                data = await response.json()
                if "current_weather" in data:
                    weather = data["current_weather"]
                    return f"🌡 Температура: {weather['temperature']}°C\n💨 Ветер: {weather['windspeed']} км/ч"
    except Exception as e:
        print(f"Ошибка получения погоды: {e}")
        return "Не удалось получить данные о погоде."


# Функция для получения случайного изображения с Unsplash
def get_random_image():
    url = "https://api.unsplash.com/photos/random"
    headers = {
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
    }
    params = {
        "query": "nature",  # Можно изменить на любой другой запрос
        "orientation": "landscape"  # Ориентация изображения
    }
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        data = response.json()
        image_url = data["urls"]["regular"]  # URL изображения
        return image_url
    except Exception as e:
        print(f"Ошибка при получении изображения: {e}")
        return None


# Команда /start
@dp.message(CommandStart())
async def start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Погода", callback_data="weather")],
        [InlineKeyboardButton(text="Фото", callback_data="photo")]
    ]
    )
    await message.reply("Привет! Выбери, что тебе нужно:", reply_markup=keyboard)


# Обработчик инлайн кнопок
@dp.callback_query(lambda c: c.data)
async def process_callback(callback_query: types.CallbackQuery):
    if callback_query.data == "weather":
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, "Введите название города, чтобы узнать погоду.")
    elif callback_query.data == "photo":
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, "Ищу фото для вас...")
        image_url = get_random_image()
        if image_url:
            await bot.send_photo(callback_query.from_user.id, image_url)
        else:
            await bot.send_message(callback_query.from_user.id, "Не удалось загрузить фото. Попробуйте позже.")


# Обработчик сообщений с городами
@dp.message(lambda message: message.text)
async def weather(message: Message):
    city_name = message.text.strip()
    lat, lon = await get_coordinates(city_name)
    if lat and lon:
        weather_info = await get_weather(lat, lon)
        await message.reply(weather_info)
    else:
        await message.reply("❌ Город не найден. Попробуйте ввести полное название (например, 'Москва, Россия').")


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
asyncio.run(main())
