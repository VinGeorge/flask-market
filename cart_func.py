from flask import session
from models import Dish


def define_cart_items(cart=False):

    cart_items = session.get("cart", [])
    dishes_in_cart = [dish for dish in Dish.query.filter(Dish.id.in_(cart_items)).all()]
    total_price = sum([dish.price for dish in dishes_in_cart])
    total_count = len(dishes_in_cart)

    if cart:
        return total_price, total_count, dishes_in_cart

    return total_price, total_count
