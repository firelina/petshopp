from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SelectField, SelectMultipleField, FieldList, widgets, \
    RadioField, DecimalField, FormField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Optional, InputRequired


class ProductForm(FlaskForm):
    tovar = BooleanField('Товар')
    amount = IntegerField('Количество', default=0)


class OrderForm(FlaskForm):
    order_number = IntegerField('Номер заказа', validators=[DataRequired()])
    created_date = DateField('Дата заказа', validators=[DataRequired()], format='%Y-%m-%d')
    customer = SelectField('Покупатель', coerce=int)
    manager = SelectField('Менеджер', coerce=int)
    tovars = FieldList(FormField(ProductForm))
    s = SubmitField("Подтвердить")


    def __init__(self, customer_choices, manager_choices,  *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.customer.choices = [(customer.id, str(customer.name + " " + customer.surname)) for customer in customer_choices]
        self.manager.choices = [(manager.id, str(manager.name + " " + manager.surname)) for manager in
                                 manager_choices]