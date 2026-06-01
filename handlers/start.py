from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from db.requests import register_user
router = Router()
WEB_APP_URL = "https://unfixable-employer-regally.ngrok-free.dev"


@router.message(CommandStart())
async def start_command(message: types.Message):
    register_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username
    )

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Відкрити магазин",
                web_app=WebAppInfo(url=WEB_APP_URL)
            )
        ]
    ])

    await message.answer(
        f"Вітаємо в інтернет магазині цифрових товарів \"Vergil's motivation\"\n"
        f"Натисніть кнопку, щоб відкрити наш магазин:",
        reply_markup=markup
    )