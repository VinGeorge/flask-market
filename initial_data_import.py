import csv
from models import Category, Dish, db


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
