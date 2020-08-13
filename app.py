from flask import Flask
import flask_migrate
import flask_sqlalchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash
from views.main import bp as main_bp
from views.cart import bp as cart_bp
from views.account import bp as account_bp
from views.login import bp as login_bp
from views.register import bp as register_bp
from views.logout import bp as logout_bp
from views.ordered import bp as order_bp

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
    password_hash = db.Column(db.String(128))
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


admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Dish, db.session))


app.register_blueprint(main_bp, url_prefix='/')
app.register_blueprint(cart_bp, url_prefix='/')
app.register_blueprint(account_bp, url_prefix='/')
app.register_blueprint(login_bp, url_prefix='/')
app.register_blueprint(register_bp, url_prefix='/')
app.register_blueprint(logout_bp, url_prefix='/')
app.register_blueprint(order_bp, url_prefix='/')


if __name__ == '__main__':
    app.run(debug=True)