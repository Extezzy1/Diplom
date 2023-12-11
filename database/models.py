import datetime

from sqlalchemy.orm import relationship, mapped_column

from .base import BaseModel
from sqlalchemy import Column, Integer, VARCHAR, Date, Boolean, ForeignKey, DateTime, Text, BigInteger, Float


class User(BaseModel):

    __tablename__ = "users"

    user_id = Column(BigInteger, nullable=False, unique=True, primary_key=True)
    first_name = Column(VARCHAR(255), nullable=True, unique=False)

    def __str__(self) -> str:
        return f"User:{self.user_id}"


class Referrals(BaseModel):

    __tablename__ = "referrals"

    referral_id = Column(BigInteger, nullable=False, unique=True, autoincrement=True, primary_key=True)
    user_id_sender = mapped_column(ForeignKey("users.user_id"))
    user_id_invited = mapped_column(ForeignKey("users.user_id"))


class Stores(BaseModel):

    __tablename__ = "stores"

    store_id = Column(BigInteger, nullable=False, unique=True, autoincrement=True, primary_key=True)
    user_id_creator = mapped_column(ForeignKey("users.user_id"))
    store_name = Column(VARCHAR(255), nullable=False)
    bot_token = Column(VARCHAR(255), nullable=False)


class UsersStore(BaseModel):

    __tablename__ = "users_store"

    user_store_id = Column(BigInteger, nullable=False, unique=True, autoincrement=True, primary_key=True)
    user_id = mapped_column(ForeignKey("users.user_id"))
    store_id = mapped_column(ForeignKey("stores.store_id"))


class Promocodes(BaseModel):

    __tablename__ = "promocodes"
    promocode_id = Column(BigInteger, nullable=False, unique=True, autoincrement=True, primary_key=True)
    store_id = mapped_column(ForeignKey("stores.store_id"))
    promocode_title = Column(VARCHAR(255), nullable=False)
    discount_percent = Column(Integer, nullable=False)


class Categories(BaseModel):

    __tablename__ = "categories"

    category_id = Column(BigInteger, nullable=False, unique=True, autoincrement=True, primary_key=True)
    category_id_fk = mapped_column(ForeignKey("categories.category_id"))
    store_id = mapped_column(ForeignKey("stores.store_id"))
    category_title = Column(VARCHAR(255), nullable=False)


class Products(BaseModel):

    __tablename__ = "products"
    product_id = Column(BigInteger, nullable=False, unique=True, autoincrement=True, primary_key=True)
    category_id = mapped_column(ForeignKey("categories.category_id"))
    product_title = Column(VARCHAR(255), nullable=False)
    product_description = Column(Text, nullable=False)
    product_price = Column(Float, nullable=False)


class ProductsPhotos(BaseModel):

    __tablename__ = "products_photos"
    file_id = Column(BigInteger, nullable=False, unique=True, primary_key=True)
    product_id = mapped_column(ForeignKey("products.product_id"))


class BasketsProducts(BaseModel):

    __tablename__ = "baskets_products"
    baskets_products_id = Column(BigInteger, nullable=False, unique=True, autoincrement=True, primary_key=True)
    user_store_id = mapped_column(ForeignKey("users_store.user_store_id"))
    product_id = mapped_column(ForeignKey("products.product_id"))


class Orders(BaseModel):

    __tablename__ = "orders"
    order_id = Column(BigInteger, nullable=False, unique=True, autoincrement=True, primary_key=True)
    user_store_id = mapped_column(ForeignKey("users_store.user_store_id"))
    value = Column(Float, nullable=False)
    payment_id = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
    payment_datetime = Column(DateTime, nullable=True)


class OrdersProducts(BaseModel):

    __tablename__ = "orders_products"

    orders_products_id = Column(BigInteger, nullable=False, unique=True, autoincrement=True, primary_key=True)
    product_id = mapped_column(ForeignKey("products.product_id"))
    order_id = mapped_column(ForeignKey("orders.order_id"))
    product_price = Column(Float, nullable=False)
