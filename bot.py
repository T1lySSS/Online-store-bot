import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from db.requests import seed_products
from handlers.start import router as start_router
from handlers.webapp import router as webapp_router
from db import engine, Base
from dotenv import load_dotenv

# 1. Настраиваем логирование
logging.basicConfig(level=logging.INFO)

# 2. СНАЧАЛА загружаем .env
load_dotenv()

# 3. ТЕПЕРЬ достаем токен и создаем бота
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():
    logging.info("Створюємо таблиці бд")
    Base.metadata.create_all(bind=engine)

    seed_products()

    logging.info("Реєстрація хендлерів")
    dp.include_router(start_router)
    dp.include_router(webapp_router)

    logging.info("Запуск бота")
    # Пропускаем накопившиеся сообщения, чтобы бот не спамил при старте
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        # Выводим реальную ошибку в консоль, чтобы понимать, если что-то пойдет не так
        logging.error(f"Помилка при роботі бота: {e}")
        logging.info("Бота було призупинено")