from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired


class CustomerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    birthday = DateField('Birthday', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Save')