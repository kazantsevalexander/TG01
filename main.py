import asyncio
from aiogram import Bot, Dispatcher, F
from googletrans import Translator
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN, WEATHER_API_KEY
import aiohttp
import os

bot = Bot(token=TOKEN)
dp = Dispatcher()
# Инициализация клиента переводчика
translator = Translator()

# Создаем папки для хранения изображений, если их нет
os.makedirs('img', exist_ok=True)
os.makedirs('tmp', exist_ok=True)

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


@dp.message(Command('voice'))
async def voice(message: Message):
    voice = FSInputFile("voices/voice.ogg")
    await message.answer_voice(voice)


@dp.message(F.photo)
async def photo(message: Message):
    await bot.download(message.photo[-1],destination=f'tmp/{message.photo[-1].file_id}.jpg')
    await message.answer('Я сохранил вашу фотку')


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


# Обработчик для перевода текста на английский язык
@dp.message()
async def translate_to_english(message: Message):
    original_text = message.text
    translated = translator.translate(original_text, src='auto', dest='en')

    await message.answer(translated.text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())