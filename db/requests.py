from sqlalchemy import select, func
from db import async_session
from db.models import User, Purchase, Product, Seller


async def register_user(telegram_id: int, username: str = None):
    async with async_session() as session:
        result = await session.execute(select(User).filter(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()
        if not user:
            new_user = User(telegram_id=telegram_id, username=username)
            session.add(new_user)
            await session.commit()
            return True
        return False


async def save_purchase(telegram_id: int, product_id: int):
    async with async_session() as session:
        new_purchase = Purchase(user_id=telegram_id, product_id=product_id)
        session.add(new_purchase)
        await session.commit()


async def get_user_purchases(telegram_id: int):
    async with async_session() as session:
        statement = (
            select(Product.name)
            .join(Purchase, Purchase.product_id == Product.id)
            .filter(Purchase.user_id == telegram_id)
        )
        result = await session.execute(statement)
        purchases = result.scalars().all()
        return list(purchases)


async def get_user_data(telegram_id: int):
    async with async_session() as session:
        result = await session.execute(select(User).filter(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()
        if not user:
            return None
        return user





async def register_seller(telegram_id: int, shop_name: str):
    async with async_session() as session:
        result = await session.execute(select(Seller).filter(Seller.user_id == telegram_id))
        seller = result.scalar_one_or_none()
        if not seller:
            new_seller = Seller(user_id=telegram_id, shop_name=shop_name)
            session.add(new_seller)
            await session.commit()
            return True
        return False


async def is_user_seller(telegram_id: int) -> bool:
    async with async_session() as session:
        result = await session.execute(select(Seller).filter(Seller.user_id == telegram_id))
        seller = result.scalar_one_or_none()
        return seller is not None


async def save_product(name: str, description: str, price: float):
    async with async_session() as session:
        new_product = Product(name=name, description=description, price=price)
        session.add(new_product)
        await session.commit()
        return True


async def get_all_products():
    async with async_session() as session:
        result = await session.execute(select(Product))
        products = result.scalars().all()

        products_list = []
        for p in products:
            products_list.append({
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "price": float(p.price)
            })
        return products_list