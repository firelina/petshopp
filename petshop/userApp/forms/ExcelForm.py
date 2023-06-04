from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField, StringField
from wtforms.fields import DateField, EmailField, TelField, FileField
from wtforms.validators import DataRequired


class ExcelForm(FlaskForm):
    file_path = StringField('Save Path', validators=[DataRequired()])