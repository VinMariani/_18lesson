# В этом финальном задании Вам предстоит написать приложение на Flask
# которое работает с двумя моделями Book и Review.
# 
#
# Для сущности Book должны быть созданы эндпоинты:
# /books        - работает с методами GET, POST
# /books/{id}   - работает с методами GET, PUT, DELETE
#
# Для сущности Review должны быть созданы эндпоинты:
# /reviews      - работает с методами GET, POST
# /reviews/{id} - работает с методами GET, PUT, DELETE
#
# Сведения для заполнения базы данных:
#
# Таблица books:
# +----+-------------------------------+---------------+------+-------+
# | id |              name             |     author    | year | pages |
# +----+-------------------------------+---------------+------+-------+
# | 1  | Гарри Поттер и Тайная Комната | Джоан Роулинг | 1990 |  400  |
# | 2  |       Граф Монте-Кристо       |      Дюма     | 1510 |  1344 |
# | 3  |  Гарри Поттер и Орден Феникса | Джоан Роулинг | 1993 |  500  |
# | 4  |   Гарри Поттер и Кубок Огня   | Джоан Роулинг | 1994 |  600  |
# +----+-------------------------------+---------------+------+-------+
#
# Таблица reviews:
# +----+-------+--------+---------+
# | id |  user | rating | book_id*|
# +----+-------+--------+---------+
# | 1  |  Oleg |   5    |    1    |
# | 2  |  Ivan |   6    |    2    |
# | 3  |  John |   4    |    3    |
# | 4  | Diana |   3    |    4    |
# +----+-------+--------+---------+
# *При создании таблицы reviews присваивать полю book_id свойство Foreign_key
#  необязательно.
#
# Структура вашего приложения должна выглядеть следующим образом:
#
# final
# ├── ./app.py         - Это главный файл, который запускает приложение
# ├── ./config.py      - Здесь мы сохраняем настройки приложения
# ├── ./constants.py   - Здесь мы сохраняем константы
# ├── ./models.py      - Здесь мы сохраняем модели
# ├── ./setup_db.py    - Здесь мы инициализируем базу данных
# ├── ./test.py        - Здесь наши тесты, запустите их, как проверите работу приложения
# └── ./views          
#     ├── ./views/books.py    - view-классы по модели Book
#     └── ./views/reviews.py  - view-классы по модели Review
#
# Пожалуйста, не меняйте название переменной 'app', которая должна 
# содержать экземпляр класса Flask, а также название переменной db,
# в которой вы инициализируете базу данных.
# это необходимо для корректной работы тестов
#
#
from flask import Flask
from config import Config
from part1.final.models import Book, Review
from setup_db import db
from flask_restx import Api
from views.books import book_ns
from views.reviews import review_ns


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.app_context().push()
    configure_app(app)
    return app


def configure_app(app):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(book_ns)
    api.add_namespace(review_ns)
    load_data(app, db)


def load_data(app, db):
    with app.app_context():
        db.drop_all()
        db.create_all()
        book1 = Book(id=1, name='Гарри Поттер и Тайная Комната', author='Джоан Роулинг', year=1990, pages=400)
        book2 = Book(id=2, name='Граф Монте-Кристо', author='Дюма', year=1510, pages=1344)
        book3 = Book(id=3, name='Гарри Поттер и Орден Феникса', author='Джоан Роулинг', year=1993, pages=500)
        book4 = Book(id=4, name='Гарри Поттер и Кубок Огня', author='Джоан Роулинг', year=1994, pages=600)
        review1 = Review(id=1, user='Oleg', rating=5, book_id=1)
        review2 = Review(id=2, user='Ivan', rating=6, book_id=2)
        review3 = Review(id=3, user='John', rating=4, book_id=3)
        review4 = Review(id=4, user='Diana', rating=3, book_id=4)
        with db.session.begin():
            db.session.add_all([book1, book2, book3, book4])
            db.session.add_all([review1, review2, review3, review4])


app_config = Config()
app = create_app(app_config)

if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)
