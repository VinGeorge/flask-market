from flask import render_template, session, Blueprint
from cart_func import define_cart_items
from models import Dish, Category


bp = Blueprint("main", __name__)


@bp.route("/")
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