import json
import base64
from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from db.requests import register_user, get_all_products  # убедись, что имя функции совпадает

router = Router()
WEB_APP_URL = "https://unfixable-employer-regally.ngrok-free.dev"  # Твоя актуальная ссылка ngrok


@router.message(CommandStart())
async def start_command(message: types.Message):
    register_user(telegram_id=message.from_user.id, username=message.from_user.username)

    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="🛒 Відкрити магазин",
                    web_app=WebAppInfo(url=WEB_APP_URL)
                )
            ]
        ],
        resize_keyboard=True
    )

    await message.answer(
        f"Вітаємо в інтернет магазині цифрових товарів \"Vergil's motivation\"\n\n"
        f"Натисніть кнопку нижче, щоб відкрити наш магазин з актуальними товарами з БД:",
        reply_markup=markup
    )