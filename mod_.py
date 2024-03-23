from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=40), unique=True)

    def __str__(self):
        return f'Publisher {self.id}: {self.name}'


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True)
    title = Column(String(length=40), unique=True)
    publisher_id = Column(Integer, ForeignKey("publisher.id"), nullable=False)

    publisher = relationship("Publisher", backref="books")

    def __str__(self):
        return f'Book {self.id}, {self.title}, {self.publisher_id}'


class Shop(Base):
    __tablename__ = "shop"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=40), unique=True)

    def __str__(self):
        return f'Shop {self.id}, {self.name}'


class Stock(Base):
    __tablename__ = "stock"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False)
    shop_id = Column(Integer, ForeignKey("shop.id"), nullable=False)
    quantity = Column(Integer)

    shop = relationship("Shop", backref="stocks")
    book = relationship("Book", backref="stocks")

    def __str__(self):
        return f'Stock {self.id}, Book: {self.book_id}, Shop: {self.shop_id}, Quantity: {self.quantity}'


class Sale(Base):
    __tablename__ = "sale"

    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    sale_date = Column(DateTime, nullable=False, server_default=sq.func.now())
    stock_id = Column(Integer, ForeignKey("stock.id"), nullable=False)
    count = Column(Integer, nullable=False)

    stock = relationship("Stock", backref="sales")

    def __str__(self):
        return f'Sale {self.id}, Price: {self.price}, Date: {self.sale_date}, Stock ID: {self.stock_id}, Count: {self.count}'


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)




