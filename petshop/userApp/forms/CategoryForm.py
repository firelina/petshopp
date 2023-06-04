from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired

class CategoryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    animal = SelectField('Animal', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Save')

    def __init__(self, animal_choices, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.animal.choices = [(animal.id, animal.specie) for animal in animal_choices]