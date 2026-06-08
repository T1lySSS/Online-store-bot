from db import Sessionlocal
from db.models import User, Purchase, Product
from db.models import Seller

def register_user(telegram_id: int, username:str = None):
    with Sessionlocal() as session:
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        if not user:
            new_user = User(telegram_id=telegram_id, username=username)
            session.add(new_user)
            session.commit()
            return True
        return False

def save_purchase(telegram_id: int, product_id: int):
    with Sessionlocal() as session:
        new_purchase = Purchase(user_id=telegram_id, product_id=product_id)
        session.add(new_purchase)
        session.commit()

def get_user_purchases(telegram_id: int):
    with Sessionlocal() as session:
        purchases = (
            session.query(Product.name)
            .join(Purchase, Purchase.product_id == Product.id)
            .filter(Purchase.user_id == telegram_id)
            .all()
        )
        return [p.name for p in purchases]

def get_user_data(telegram_id: int):
    with Sessionlocal() as session:
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        if not user:
            return None
        return user


def seed_products():
    with Sessionlocal() as session:
        if session.query(Product).count() == 0:
            products = [
                Product(name="🔥 Motivation Pack", description="Повний пакет мотивації від Вергілія. Додає +100% до швидкості коду.", price=150.0),
                Product(name="⚡ Yamato Digital Link", description="Цифровий сертифікат на володіння легендарним мечем Ямато.", price=300.0),
                Product(name="👑 Premium Status", description="Преміум статус у всесвіті Devil May Cry. Доступ до ексклюзивних мемів.", price=500.0),
            ]
            session.add_all(products)
            session.commit()
            print("База даних успішно заповнена тестовими товарами!")

def register_seller(telegram_id: int, shop_name: str):
    with Sessionlocal() as session:
        seller = session.query(Seller).filter(Seller.user_id == telegram_id).first()
        if not seller:
            new_seller = Seller(user_id=telegram_id, shop_name=shop_name)
            session.add(new_seller)
            session.commit()
            return True
        return False

def is_user_seller(telegram_id: int) -> bool:
    with Sessionlocal() as session:
        seller = session.query(Seller).filter(Seller.user_id == telegram_id).first()
        return seller is not None

def save_product(name:str, description:str, price:float):
    with Sessionlocal() as session:
        new_product = Product(name=name,
                              description=description,
                              price=price)
        session.add(new_product)
        session.commit()
        return True


def get_all_products():
    with Sessionlocal() as session:
        products = session.query(Product).all()

        products_list = []

        for p in products:
            products_list.append({
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "price": float(p.price)
            })

        return products_list
