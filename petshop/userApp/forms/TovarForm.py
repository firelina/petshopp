from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, NumberRange


class TovarForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    cost = IntegerField('Cost', validators=[DataRequired(), NumberRange(min=1)])
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Save')

    def __init__(self, category_choices, *args, **kwargs):
        super(TovarForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, str(category.title + " для " + category.animal.specie)) for category in category_choices]

    def validate(self):
        initial_validation = super(TovarForm, self).validate()
        if not initial_validation:
            return False
        if self.cost.data <= 0:
            self.cost.errors.append('Cost must be greater than 0')
            return False
        return True