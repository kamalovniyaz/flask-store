from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class LoginForm:
    email = StringField("Email: ", validators=[Email()])
    password = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=6, max=100)])
    remember = BooleanField("Запомнить", default=False)
    submit = SubmitField("Войти")