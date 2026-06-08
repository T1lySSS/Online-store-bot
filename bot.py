import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from db.requests import seed_products
from handlers.start import router as start_router
from handlers.webapp import router as webapp_router
from handlers.payments import router as payments_router
from handlers.seller import router as seller_router
from handlers.add_product import router as addproduct_router
from db import engine, Base
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO)


load_dotenv()

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
    dp.include_router(payments_router)
    dp.include_router(seller_router)
    dp.include_router(addproduct_router)
    logging.info("Запуск бота")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"Помилка при роботі бота: {e}")
        logging.info("Бота було призупинено")