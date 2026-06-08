from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from db.requests import register_seller, is_user_seller, register_user

router = Router()



class SellerRegistration(StatesGroup):
    waiting_for_shop_name = State()


@router.message(Command("register_seller"))
async def start_seller_reg(message: types.Message, state: FSMContext):
    user_id = message.from_user.id


    if is_user_seller(user_id):
        await message.answer("❌ Ви вже зареєстровані як продавець у нашій системі!")
        return


    await register_user(telegram_id=user_id, username=message.from_user.username)

    await message.answer("🏪 **Реєстрація аккаунта продавця**\n\nБудь ласка, введіть назву вашого майбутнього магазину:")

    await state.set_state(SellerRegistration.waiting_for_shop_name)


@router.message(SellerRegistration.waiting_for_shop_name)
async def process_shop_name(message: types.Message, state: FSMContext):
    shop_name = message.text.strip()
    user_id = message.from_user.id

    if len(shop_name) < 3:
        await message.answer("❌ Назва магазину занадто коротка (мінімум 3 символи). Спробуйте ще раз:")
        return


    success = register_seller(telegram_id=user_id, shop_name=shop_name)

    if success:
        await message.answer(
            f"🎉 **Вітаємо!**\n\n"
            f"Ваш аккаунт продавця успішно створено.\n"
            f"Назва магазину: **{shop_name}**\n\n"
            f"Тепер ви маєте статус партнера в системі!"
        )
    else:
        await message.answer("Щось пішло не так, або ви вже є продавцем.")


    await state.clear()