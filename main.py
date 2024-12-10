import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN, WEATHER_API_KEY
import requests
import aiohttp

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция для получения прогноза погоды
import requests


async def get_weather():
    city_id = 625144  # Minsk's city ID
    url = f"https://api.openweathermap.org/data/2.5/weather?id={city_id}&units=metric&lang=ru&appid={WEATHER_API_KEY}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()  # Raise HTTPError for bad responses
                return await response.json()
    except aiohttp.ClientError as e:
        return {"error": str(e)}

# Command to get the weather forecast
@dp.message(Command('weather'))
async def weather(message: Message):
    weather_data = await get_weather()

    if "error" in weather_data:
        await message.answer(f"Error: {weather_data['error']}")
    else:
        description = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']
        response_text = f"Погода в минске: {temperature}°C, {description}."
        await message.answer(response_text)


@dp.message(F.text == 'Когда основан Минск?')
async def aitext(message: Message):
    await message.answer('Минск - один из старейших городов Европы. '
                         'Первое письменное упоминание датируется 1067 годом.')


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет предсказывать погоду в Минске и комманды: \n /start \n /help \n /weather\n'
                         'и еще ты можешь сросить "Когда основан Минск?"')

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Приветики, я бот!")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())