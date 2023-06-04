from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, DateField, BooleanField
# from wtforms.fields.html5 import EmailField
from wtforms.fields import DateField, EmailField, TelField, SelectField
from wtforms.validators import DataRequired


# форма для регистрации
class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    lastname = StringField('Отчество', validators=[DataRequired()])
    telethon = StringField('Телефон', validators=[DataRequired()])
    birthday = DateField('День рождения', validators=[DataRequired()], format='%Y-%m-%d')
    login = StringField('Логин', validators=[DataRequired()])
    role = BooleanField('Администратор')
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')
