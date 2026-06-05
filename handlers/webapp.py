import json
import os
from aiogram import Router, F, types
from aiogram.types import LabeledPrice
from handlers.payments import PROVIDER_TOKEN

router = Router()


@router.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
    raw_data = message.web_app_data.data

    try:
        data = json.loads(raw_data)

        if data.get("action") == "buy":
            product_id = int(data.get("product_id"))
            product_name = data.get("product_name")


            price_map = {1: 15000, 2: 30000, 3: 50000}
            product_price = price_map.get(product_id, 10000)


            await message.bot.send_invoice(
                chat_id=message.chat.id,
                title=f"Купівля: {product_name}",
                description=f"Оплата цифрового доступу до продукту {product_name} для курсового проекту.",
                payload=f"product_id_{product_id}",
                provider_token=PROVIDER_TOKEN,
                currency="UAH",
                prices=[
                    LabeledPrice(label=product_name, amount=product_price)
                ],
                start_parameter="motivation-store-payment"
            )

    except Exception as e:
        await message.answer("Виникла помилка при генерації рахунку.")
        print(f"Ошибка в webapp handler: {e}")