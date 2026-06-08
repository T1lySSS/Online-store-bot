from datetime import datetime
# Обов'язково імпортуємо BigInteger
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, BigInteger
from db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # Змінюємо Integer на BigInteger
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String, nullable=True)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    image_url = Column(String, nullable=True)

class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    # Змінюємо на BigInteger, бо посилається на users.telegram_id
    user_id = Column(BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    purchased_at = Column(DateTime, default=datetime.utcnow)

class Seller(Base):
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True, index=True)
    # Змінюємо на BigInteger
    user_id = Column(BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE"), unique=True, nullable=False)
    shop_name = Column(String, nullable=False)
    registered_at = Column(DateTime, default=datetime.utcnow)