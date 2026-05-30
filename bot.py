import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from handlers.start import router as start_router
from db import engine, Base
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)


BOT_TOKEN = os.getenv("BOT_TOKEN")

load_dotenv()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def main():
    logging.info("Створюємо таблиці бд")
    Base.metadata.create_all(bind=engine)
    logging.info("Реєстрація хендлерів")
    dp.include_router(start_router)
    logging.info("Запуск бота")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        logging.info("Бота було призупинено")
