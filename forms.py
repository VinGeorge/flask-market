from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField
from wtforms.validators import InputRequired, Email, Length


class RegistrationForm(FlaskForm):

    usermail = StringField("Электропочта", [Email(message="Кажется это не почта. Попробуйте еще раз!"),
                                            InputRequired()])
    password = PasswordField("Пароль", [InputRequired(message="Введите пароль. Без него сейчас никак")])


class OrderForm(FlaskForm):

    usermail = StringField("Электропочта", [Email(message="Кажется это не почта. Попробуйте еще раз!"),
                                            InputRequired(), Length(5)])
    name = StringField("Ваше имя", [InputRequired()])
    adress = StringField("Адрес", [InputRequired()])
    phone = StringField("Телефон", [InputRequired()])
    userOrder = HiddenField("userOrder")
    order_sum = HiddenField("orderSum")