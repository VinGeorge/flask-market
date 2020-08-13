from flask import render_template, request, session, redirect, Blueprint
from forms import RegistrationForm
from models import User


bp = Blueprint("login", __name__)


@bp.route('/login/', methods=["GET", "POST"])
def login():

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

        if user.password_valid(password):
            session['id'] = user.id
            session['mail'] = user.mail
            return redirect('/account/')
        else:

            error_msg = "Неправильно указана почта или пароль"
            return render_template("login.html", form=form, error_msg=error_msg)

    return render_template('login.html', form=form)