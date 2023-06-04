from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError


class ProviderForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    telethon = StringField('Telethon', validators=[DataRequired()])
    submit = SubmitField('Save')

    # def __init__(self, provider=None, *args, **kwargs):
    #     super(ProviderForm, self).__init__(*args, **kwargs)
    #     self.provider = provider
    #     if provider:
    #         self.title.data = provider.title
    #         self.telethon.data = provider.telethon

