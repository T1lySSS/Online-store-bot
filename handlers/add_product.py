from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from db.requests import is_user_seller, register_user, save_product
router = Router()

class ProductRegistration(StatesGroup):
    add_name_state = State()
    add_description_state = State()
    add_price_state = State()
@router.message(Command("add_product"))
async def add_product_command(message: Message, state: FSMContext):
    await state.clear()
    register_user(message.from_user.id, message.from_user.username)
    if not is_user_seller(message.from_user.id):
        await message.answer("Ви не являєтеся продавцем.\n"
                             "Будь ласка, зареєструйте акаунт продавця через команду /register_seller, аби мати можливість додати товар у магазин.")
        return

    await state.set_state(ProductRegistration.add_name_state)
    await message.answer("Введіть назву продукту:")

@router.message(ProductRegistration.add_name_state)
async def write_product_name(message: Message, state: FSMContext):
    await state.update_data(product_name=message.text)
    await state.set_state(ProductRegistration.add_description_state)
    await message.answer("Введіть опис товару: ")

@router.message(ProductRegistration.add_description_state)
async def write_product_description(message: Message, state: FSMContext):
    await state.update_data(product_description=message.text)
    await state.set_state(ProductRegistration.add_price_state)
    await message.answer("Введіть ціну товару: ")

@router.message(ProductRegistration.add_price_state)
async def write_product_price(message: Message, state: FSMContext):
    price_text = message.text.replace(",", ".")
    try:
        price = float(price_text)
        state_data = await state.get_data()
        name = state_data.get("product_name")
        description = state_data.get("product_description")
        save_product(name, description, price)
        await state.clear()
        await message.answer("Ваш товар було додано!")


    except ValueError:
        await message.answer("Будь ласка, введіть ціну товару у вигляді дійсного числа")