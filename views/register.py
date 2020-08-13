from flask import render_template, request, Blueprint
from forms import RegistrationForm
from models import User, db


bp = Blueprint("register", __name__)


@bp.route('/register/', methods=["GET", "POST"])
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
            password_hash=password
        ))
        db.session.commit()

        return f'Спасибо за регистрацию!'

    return render_template("register.html", form=form, error_msg=error_msg)
