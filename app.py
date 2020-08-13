from flask import Flask
import os
import flask_migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import User, Order, Dish, User, Category, db
from market_views.main import bp as main_bp
from market_views.cart import bp as cart_bp
from market_views.account import bp as account_bp
from market_views.login import bp as login_bp
from market_views.register import bp as register_bp
from market_views.logout import bp as logout_bp
from market_views.ordered import bp as order_bp


app = Flask(__name__)  # объявим экземпляр фласка
app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
migrate = flask_migrate.Migrate(app, db)


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
    app.run()