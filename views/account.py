from flask import render_template, session, Blueprint
from models import Order, User, Dish, orders_asso, db
from cart_func import define_cart_items

bp = Blueprint("account", __name__)


categories_file = 'data/delivery_categories.csv'
dishes_file = 'data/delivery_items.csv'


@bp.route('/account/', methods=["GET"])
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