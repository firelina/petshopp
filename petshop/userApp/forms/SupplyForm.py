from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SelectField, SelectMultipleField, FieldList, widgets, \
    RadioField, DecimalField, FormField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Optional, InputRequired


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class ProductForm(FlaskForm):
    tovar = BooleanField('Товар')
    amount = IntegerField('Количество', default=0)


class SupplyForm(FlaskForm):
    supply_number = IntegerField('Номер поставки', validators=[DataRequired()])
    created_date = DateField('Дата поставки', validators=[DataRequired()], format='%Y-%m-%d')
    provider = SelectField('Поставщик', coerce=int)
    manager = SelectField('Менеджер', coerce=int)
    tovars = FieldList(FormField(ProductForm))
    # tovars = SelectField('Товары', coerce=int)
    # tovars = SelectMultipleField("Товары", coerce=int, validators=[DataRequired()], render_kw={'multiple': True})
    s = SubmitField("Подтвердить")



    def __init__(self, provider_choices, manager_choices, tovar_choices,  *args, **kwargs):
        super(SupplyForm, self).__init__(*args, **kwargs)
        self.provider.choices = [(provider.id, provider.title) for provider in provider_choices]
        self.manager.choices = [(manager.id, str(manager.name + " " + manager.surname)) for manager in
                                 manager_choices]
        self.tovars.choices = [(tovar.id, str(tovar.title + " " + tovar.category.title + " " + tovar.category.animal.specie)) for
                      tovar in tovar_choices]

        # self.tovars.min_entries = num
