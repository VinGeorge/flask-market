from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import flask_sqlalchemy
import flask_migrate
import csv

app = Flask(__name__)
app.config["DEBUG"] = True
app = Flask(__name__)  # объявим экземпляр фласка
app.secret_key = "randomstring"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://stmafswldqtivy:1fa95bb194a917926b3a0343a4b6157c15c67f3457cf08bf1df63601d01bd463@ec2-54-197-254-117.compute-1.amazonaws.com:5432/d18md6kmp2cikr'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = flask_sqlalchemy.SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)


orders_asso = db.Table('orders_asso',
                      db.Column('order_id', db.Integer, db.ForeignKey('orders.id')),
                      db.Column('dish_id', db.Integer, db.ForeignKey('dishes.id'))
                      )


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    orders = db.relationship('Order')


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
    date = db.Column(db.Date, nullable=False)
    order_sum = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, nullable=False)
    mail = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    adress = db.Column(db.String, nullable=False)
    dishes = db.relationship('Dish',
                            secondary=orders_asso,
                            back_populates='orders')
    user = db.relationship('User')
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


categories_file = 'data/delivery_categories.csv'
dishes_file = 'data/delivery_items.csv'


def import_categories():

    with open(categories_file, 'r') as f:
        categories = csv.DictReader(f, delimiter=',')
        for category in categories:
            db.session.add(Category(
                title=category['title']
            ))

    db.session.commit()


def import_dishes():

    with open(dishes_file, 'r') as f:
        dishes = csv.DictReader(f, delimiter=',')
        for dish in dishes:
            db.session.add(Dish(
                title=dish['title'],
                price=dish['price'],
                description=dish['description'],
                picture=dish['picture'],
                category_id=dish['category_id']
            ))
    db.session.commit()


@app.route('/')
def main():

    categories = [category for category in Category.query.all()]
    dishes = [dish for dish in Dish.query.all()]


    return render_template('main.html', dishes=dishes, categories=categories)


@app.route('/cart/')
def cart():

    return render_template('cart.html')


@app.route('/account/')
def account():

    return render_template('account.html')


@app.route('/login/')
def login():

    return render_template('login.html')


@app.route('/register/')
def register():

    return render_template('register.html')


@app.route('/logout/')
def logout():

    return render_template('main.html')


@app.route('/ordered/')
def ordered():

    return render_template('ordered.html')



if __name__ == '__main__':
    # import_categories()
    # import_dishes()
    # print(Dish.query.count())
    # Dish.query.delete()
    # Category.query.delete()
    # db.session.commit()
    app.run(debug=True)