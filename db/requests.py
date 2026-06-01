from db import Sessionlocal
from db.models import User, Purchase, Product


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