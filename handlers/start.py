from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, MenuButtonWebApp, KeyboardButton, ReplyKeyboardMarkup

router = Router()

@router.message(F.text == "/start")
async def start_cmd(message: Message):

    web_app_url = "https://unfixable-employer-regally.ngrok-free.dev"


    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="🛒 Відкрити магазин",
                    web_app=WebAppInfo(url=web_app_url)
                )
            ]
        ],
        resize_keyboard=True
    )


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
        f"Вітаємо в інтернет магазині цифрових товарів Vergil's motivation"
        f"Натисніть кнопку нижче, щоб відкрити наш магазин",
        reply_markup=markup,
    )
    await message.answer(
        f".",
        reply_markup=kb
    )