from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

router = Router()

@router.message(F.text == "/start")
async def start_cmd(message: Message):

    web_app_url = "https://unfixable-employer-regally.ngrok-free.dev"


    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🛒 Відкрити магазин",
                    web_app=WebAppInfo(url=web_app_url)
                )
            ]
        ]
    )

    await message.answer(
        "Вітаємо в інтернет-магазині цифрових товарів \"Vergil's motivation\"\n\n"
        "Натисніть кнопку нижче, щоб відкрити наш магазин з актуальними товарами з БД:",
        reply_markup=kb
    )