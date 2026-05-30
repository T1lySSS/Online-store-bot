from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

router = Router()
WEB_APP_URL = "https://www.google.com"

@router.message(CommandStart())
async def start_command(message: types.Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Відкрити магазин",
                web_app=WebAppInfo(url=WEB_APP_URL)
            )
        ]
    ])
    await message.answer(
        f'Вітаємо в інтернет магазині цифрових товарів "Vergil`s motivation"\n'
        f'Натисніть кнопку, щоб відкрити наш магазин:',
        reply_markup=markup
    )