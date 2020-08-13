from flask import render_template, session, redirect, url_for, Blueprint
from forms import OrderForm
from cart_func import define_cart_items


bp = Blueprint("cart", __name__)


@bp.route('/cart/', methods=["GET", "POST"])
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


@bp.route('/addtocart/<int:dish_id>', methods=["GET"])
def add_to_cart(dish_id):

    cart = session.get("cart", [])
    cart.append(dish_id)
    session['cart'] = cart

    return redirect("/cart/")


@bp.route('/removefromcart/<int:dish_id>', methods=["GET"])
def remove_from_cart(dish_id):

    remove_status = False
    cart = session.get("cart", [])
    cart.remove(dish_id)
    session['cart'] = cart

    if len(cart) == 0:

        return redirect("/")

    if session.get("cart"):
        remove_status = True

    return redirect(url_for(endpoint='cart.cart', remove_status=remove_status))
