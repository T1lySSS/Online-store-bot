import json
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
            product_name = data.get("product_name")
            product_price = int(data.get("price"))

            await message.bot.send_invoice(
                chat_id=message.chat.id,
                title=f"Купівля: {product_name}",
                description=f"Оплата доступу до {product_name} для курсового проекту.",
                payload=f"product_{data.get('product_id')}",
                provider_token=PROVIDER_TOKEN,
                currency="UAH",
                prices=[
                    LabeledPrice(label=product_name, amount=product_price)
                ],
                start_parameter="motivation-store-payment"
            )

    except Exception as e:
        await message.answer("Виникла помилка при генерації рахунку.")
        print(f"Помилка в webapp handler: {e}")