import os


from aiogram import Router, F
from aiogram.types import PreCheckoutQuery, Message
from db.requests import save_purchase
router = Router()

PROVIDER_TOKEN = os.getenv("PROVIDER_TOKEN")


@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def process_successful_payment(message: Message):
    payload = message.successful_payment.invoice_payload

    product_id = int(payload.split("_")[-1])
    user_id = message.from_user.id

    save_purchase(telegram_id=user_id, product_id=product_id)

    await message.answer(
        f"💳 **Оплата успішна!**\n\n"
        f"Дякуємо за покупку. Товар успішно додано до вашої бази даних та активовано в профілі Mini App!"
    )