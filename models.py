from flask import Flask
import flask_migrate
import flask_sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = flask_sqlalchemy.SQLAlchemy()


orders_asso = db.Table('orders_asso',
                      db.Column('order_id', db.Integer, db.ForeignKey('orders.id')),
                      db.Column('dish_id', db.Integer, db.ForeignKey('dishes.id'))
                      )


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    orders = db.relationship('Order')

    @property
    def password(self):
        # Запретим прямое обращение к паролю
        raise AttributeError("Вам не нужно знать пароль!")

    @password.setter
    def password(self, password):
        # Устанавливаем пароль через этот метод
        self.password_hash = generate_password_hash(password)

    def password_valid(self, password):
        # Проверяем пароль через этот метод
        # Функция check_password_hash превращает password в хеш и сравнивает с хранимым
        return check_password_hash(self.password_hash, password)


class Dish(db.Model):
    __tablename__ = 'dishes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=False)
    category = db.relationship('Category')
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    orders = db.relationship('Order',
                             secondary=orders_asso,
                             back_populates='dishes')


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    dish = db.relationship('Dish')


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_sum = db.Column(db.Float, nullable=False)
    mail = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    order_date = db.Column(db.Date, nullable=False)
    adress = db.Column(db.String, nullable=False)
    dishes = db.relationship('Dish',
                             secondary=orders_asso,
                             back_populates='orders')
    user = db.relationship('User')
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
