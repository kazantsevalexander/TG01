import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from config import TOKEN
import logging


bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Приветики, я бот!")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())