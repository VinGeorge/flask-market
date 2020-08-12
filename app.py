from flask import Flask, render_template, request, session, redirect, url_for
import flask_sqlalchemy
import flask_migrate
import csv
from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField
from wtforms.validators import InputRequired, Email

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


class RegistrationForm(FlaskForm):

    usermail = StringField("Электропочта", [Email(message="Кажется это не почта. Попробуйте еще раз!"), InputRequired()])
    password = PasswordField("Пароль", [InputRequired(message="Введите пароль. Без него сейчас никак")])


class OrderForm(FlaskForm):

    usermail = StringField("Электропочта", [Email(message="Кажется это не почта. Попробуйте еще раз!"), InputRequired()])
    name = StringField("Ваше имя", [InputRequired()])
    adress = StringField("Адрес", [InputRequired()])
    phone = StringField("Телефон", [InputRequired()])
    userOrder = HiddenField("userOrder")
    order_sum = HiddenField("orderSum")


def define_cart_items(cart=False):

    cart_items = session.get("cart", [])
    dishes_in_cart = [dish for dish in Dish.query.filter(Dish.id.in_(cart_items)).all()]
    total_price = sum([dish.price for dish in dishes_in_cart])
    total_count = len(dishes_in_cart)

    if cart:
        return total_price, total_count, dishes_in_cart

    return total_price, total_count


@app.route('/')
def main():

    total_price, total_count = define_cart_items()
    categories = [category for category in Category.query.all()]
    dishes = [dish for dish in Dish.query.all()]

    try:
        session['id']
        login_status = True
    except KeyError:
        login_status = False

    return render_template('main.html', dishes=dishes, categories=categories, total_price=total_price,
                           total_count=total_count, login_status=login_status)


@app.route('/cart/', methods=["GET", "POST"])
def cart():

    total_price, total_count, dishes = define_cart_items(cart=True)
    dishes_id = [dish.id for dish in dishes]
    form = OrderForm(userOrder=dishes_id, order_sum=total_price)

    try:
        session['id']
        login_status = True
    except KeyError:
        login_status = False

    return render_template('cart.html', dishes=dishes, total_count=total_count, total_price=total_price,
                           login_status=login_status, form=form)


@app.route('/account/', methods=["GET"])
def account():

    try:

        user_dishes = db.session.query(Order.id, Order.order_date, Order.order_sum, Dish.title, Dish.price) \
            .select_from(Order).join(orders_asso).join(Dish).join(User).filter(User.id == session['id']).all()

        total_price, total_count = define_cart_items()

        user_orders = db.session.query(Order.id, Order.order_date, Order.order_sum).select_from(Order) \
            .join(User).filter(User.id == session['id']).all()

        login_status = True

        return render_template('account.html', total_price=total_price, total_count=total_count,
                               user_orders=user_orders, user_dishes=user_dishes, login_status=login_status)

    except KeyError:
        return f"Только зарегистрированным пользователям доступен личный кабинет"



@app.route('/login/', methods=["GET", "POST"])
def login():

    error_msg = ""

    form = RegistrationForm()

    if request.method == "POST":

        usermail = request.form.get("usermail")
        password = request.form.get("password")
        user = User.query.filter_by(mail=usermail).first()

        if not usermail or not password:
            error_msg = "Не указано имя или пароль"
            return render_template("login.html", form=form, error_msg=error_msg)

        if user is False:
            error_msg = "Пользователь с такой почтой не найден"
            return render_template("login.html", form=form, error_msg=error_msg)

        if user.password != password:
            error_msg = "Неправильно указана почта или пароль"
            return render_template("login.html", form=form, error_msg=error_msg)

        session['id'] = user.id
        session['mail'] = user.mail
        return redirect('/')

    return render_template('login.html', form=form)


@app.route('/register/', methods=["GET", "POST"])
def register():

    error_msg = ""

    form = RegistrationForm()

    if request.method == "POST":

        usermail = request.form.get("usermail")
        password = request.form.get("password")
        user = User.query.filter_by(mail=usermail).first()

        if not usermail or not password:

            error_msg = "Не указано имя или пароль"
            return render_template("register.html", form=form, error_msg=error_msg)

        if user:
            error_msg = "Пользователь с такой почтой уже существует"
            return render_template("register.html", form=form, error_msg=error_msg)

        db.session.add(User(
            mail=usermail,
            password=password
        ))
        db.session.commit()

        return f'Спасибо за регистрацию!'

    return render_template("register.html", form=form, error_msg=error_msg)


@app.route('/addtocart/<int:dish_id>', methods=["GET"])
def add_to_cart(dish_id):

    cart = session.get("cart", [])
    cart.append(dish_id)
    session['cart'] = cart

    return redirect("/cart/")


@app.route('/removefromcart/<int:dish_id>', methods=["GET"])
def remove_from_cart(dish_id):

    cart = session.get("cart", [])
    cart.remove(dish_id)
    session['cart'] = cart

    if len(cart) == 0:

        return redirect("/")

    if session.get("cart"):
        remove_status = True

    return redirect(url_for(endpoint='cart', remove_status=remove_status))


@app.route('/logout/')
def logout():

    session.pop('id')
    session.pop('mail')

    return redirect('/')


@app.route('/ordered/', methods=["POST", "GET"])
def ordered():

    form = OrderForm()

    if request.method == 'POST':

        mail = form.usermail.data
        adress = form.adress.data
        phone = form.phone.data
        orderSum = form.order_sum.data
        orderDate = date.today()

        user_id = session['id']
        user = User.query.filter_by(id=user_id).first()

        if user:
            new_order = Order(
                mail=mail,
                adress=adress,
                phone=phone,
                order_sum=orderSum,
                order_date=orderDate,
                user=user)

            db.session.add(new_order)

        else:
            new_order = Order(
                mail=mail,
                adress=adress,
                phone=phone,
                order_sum=orderSum,
                order_date=orderDate)

            db.session.add(new_order)

        for dish_id in session['cart']:
            dish = Dish.query.filter_by(id=dish_id).first()
            dish.orders.append(new_order)

        db.session.commit()

    return render_template('ordered.html')



if __name__ == '__main__':
    app.run(debug=True)