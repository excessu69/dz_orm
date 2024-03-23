import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from mod_ import create_tables, Publisher, Book, Shop, Stock, Sale

DSN = 'postgresql://postgres:Qgpd146itT78$@localhost:5432/book_shop'
engine = sq.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

def fill_tables_with_data():

    publishers = [Publisher(name='Пушкин'), Publisher(name='Булгаков')]
    session.add_all(publishers)
    session.commit()

    # Добавляем книги
    books = [
        Book(title='Капитанская дочка', publisher_id=1),
        Book(title='Руслан и Людмила', publisher_id=1),
        Book(title='Евгений Онегин', publisher_id=1),
        Book(title='Мастер и Маргарита', publisher_id=2),
        Book(title='Собачье сердце', publisher_id=2),
        Book(title='Морфий', publisher_id=2),

    ]
    session.add_all(books)
    session.commit()

    # Добавляем магазины
    shops = [Shop(name='Буквоед '), Shop(name=' Лабиринт'), Shop(name='Книжный дом')]
    session.add_all(shops)
    session.commit()

    # Добавляем запасы книг в магазины
    stocks = [
        Stock(book_id=1, shop_id=1, quantity=10),
        Stock(book_id=2, shop_id=1, quantity=5),
        Stock(book_id=3, shop_id=2, quantity=8),
        Stock(book_id=4, shop_id=3, quantity=5),
        Stock(book_id=5, shop_id=3, quantity=8),
        Stock(book_id=6, shop_id=1, quantity=10),
        Stock(book_id=1, shop_id=2, quantity=5),
        Stock(book_id=2, shop_id=3, quantity=8),
        Stock(book_id=6, shop_id=3, quantity=10)
    ]
    session.add_all(stocks)
    session.commit()

    # Добавляем продажи
    sales = [
        Sale(price=100, sale_date=datetime(2023, 1, 1), stock_id=1, count=5),
        Sale(price=150, sale_date=datetime(2023, 1, 2), stock_id=2, count=3),
        Sale(price=200, sale_date=datetime(2023, 1, 3), stock_id=3, count=4),
        Sale(price=100, sale_date=datetime(2023, 1, 1), stock_id=4, count=5),
        Sale(price=150, sale_date=datetime(2023, 1, 2), stock_id=5, count=3),
        Sale(price=150, sale_date=datetime(2023, 1, 3), stock_id=6, count=7),
        Sale(price=300, sale_date=datetime(2023, 1, 3), stock_id=7, count=4),
        Sale(price=200, sale_date=datetime(2023, 1, 3), stock_id=8, count=6),
        Sale(price=400, sale_date=datetime(2023, 1, 3), stock_id=9, count=4),
    ]
    session.add_all(sales)
    session.commit()

if __name__ == "__main__":
    fill_tables_with_data()




def data_output():
    publisher_name = input("Введите имя автора: ")

    publisher = session.query(Publisher).filter(Publisher.name == publisher_name).first()

    if publisher:

        sales = session.query(Sale).join(Stock, Sale.stock_id == Stock.id)\
                                   .join(Book, Stock.book_id == Book.id)\
                                   .join(Shop, Stock.shop_id == Shop.id)\
                                   .filter(Book.publisher_id == publisher.id)\
                                   .all()

        for sale in sales:
            print(f"{sale.stock.book.title} | {sale.stock.shop.name} | {sale.price} | {sale.sale_date.strftime('%d-%m-%Y')}")

    else:
        print("Издатель с таким именем не найден.")


if __name__ == "__main__":
    data_output()