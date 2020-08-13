from flask import render_template, request, session, Blueprint
from forms import OrderForm
from datetime import date
from models import User, Order, Dish, User, db

bp = Blueprint("ordered", __name__)


@bp.route('/ordered/', methods=["POST", "GET"])
def ordered():

    form = OrderForm()

    if request.method == 'POST':

        mail = form.usermail.data
        adress = form.adress.data
        phone = form.phone.data
        orderSum = form.order_sum.data
        orderDate = date.today()

        try:
            user = User.query.filter_by(id=session['id']).first()
            login_status = True

        except KeyError:
            login_status = False

        if login_status:
            new_order = Order(
                mail=mail,
                adress=adress,
                phone=phone,
                order_sum=orderSum,
                order_date=orderDate,
                user=user)

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
