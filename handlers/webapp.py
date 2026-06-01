import json
from aiogram import Router, F, types
from db.requests import save_purchase

router = Router()


@router.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
    raw_data = message.web_app_data.data

    try:
        data = json.loads(raw_data)

        if data.get("action") == "buy":
            product_id = int(data.get("product_id"))
            product_name = data.get("product_name")
            user_id = message.from_user.id
            save_purchase(telegram_id=user_id, product_id=product_id)
            await message.answer(
                f"🎉 **Успішна покупка!**\n\n"
                f"Ви придбали товар: **{product_name}**\n"
                f"Дякуємо за замовлення! Товар додано у ваш профіль в Mini App."
            )

    except Exception as e:
        await message.answer("Виникла помилка при обробці замовлення.")
        print(f"Ошибка в webapp handler: {e}")