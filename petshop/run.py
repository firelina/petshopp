import json

import pandas as pd
from flask import request, render_template, redirect, url_for, jsonify
import requests
from flask.json import JSONEncoder
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask_excel import make_response_from_array
import os
import openpyxl
from tkinter import filedialog
import tkinter as tk

# from petshop.userApp.database.Supply import supply_tovar_table
from sqlalchemy import select, func

from petshop.userApp.forms.AnimalForm import AnimalForm
from petshop.userApp.forms.CategoryForm import CategoryForm
from petshop.userApp.forms.CustomerForm import CustomerForm
from petshop.userApp.forms.ExcelForm import ExcelForm
from petshop.userApp.forms.ManagerForm import ManagerForm
from petshop.userApp.forms.OrderForm import OrderForm
from petshop.userApp.forms.ProviderForm import ProviderForm
from petshop.userApp.forms.SupplyForm import SupplyForm, ProductForm
from petshop.userApp.forms.TovarForm import TovarForm
from userApp import userApp
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import MultiDict

from config import config

login_manager = LoginManager()
login_manager.init_app(userApp)

userApp.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE']['URI']
userApp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(userApp)
from userApp.database import *
db.create_all()


def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user


# служебная функция загрузки пользователя
@login_manager.user_loader
def load_user(user_id):
    return get_user(user_id)


@userApp.route('/')
@userApp.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(f'/{current_user.id}')
        # return flask.render_template("main_page.html", user_id=current_user.id)
    else:
        return render_template("index.html")


from userApp.forms import *
# регистрация пользователя


@userApp.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return flask.render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        if User.query.filter_by(email = form.email.data).first():
            return flask.render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        manager = Manager(name=form.name.data, surname=form.surname.data, lastname=form.lastname.data,
                          telethon=form.telethon.data, birthday=form.birthday.data)
        user = User(login=form.login.data, email=form.email.data, role=form.role.data)
        user.manager = manager
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.add(manager)
        db.session.commit()

        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


# вход пользователя в систему
@userApp.route('/login', methods=['GET', 'POST'])
def login():
    global my_id
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            my_id = user.id
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


# выход с сайта
@userApp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@userApp.route('/<int:id>')
@login_required
def user_page(id):
    # animal = db.session.query(Animal).get(id)
    return render_template("user_page.html", res=current_user.manager)


@userApp.route('/start', methods=('GET', 'POST'))
@login_required
def start():
    return render_template("start.html")


@userApp.route('/order', methods=('GET', 'POST'))
@login_required
def order():
    return render_template("order.html")


@userApp.route('/supply', methods=('GET', 'POST'))
@login_required
def supply():
    return render_template("supply.html")


@userApp.route('/manager', methods=('GET', 'POST'))
@login_required
def manager():
    return render_template("manager.html")


@userApp.route('/sort_store', methods=('GET', 'POST'))
@login_required
def sort_store():
    results = db.session.execute(select(Tovar.title, Tovar.cost, Store.amount).join(Store, Tovar.store_id == Store.id).order_by(Tovar.title)).fetchall()
    return render_template("store.html", products=results)


@userApp.route('/store', methods=('GET', 'POST'))
@login_required
def store():
    results = db.session.execute(select(Tovar.title, Tovar.cost, Store.amount).join(Store, Tovar.store_id == Store.id)).fetchall()
    return render_template("store.html", products=results)


@userApp.route('/excel_store', methods=('GET', 'POST'))
@login_required
def excel_store():
    results = db.session.execute(
        select(Tovar.title, Tovar.cost, Store.amount).join(Store, Tovar.store_id == Store.id)).fetchall()
    df = pd.DataFrame(results, columns=["Tovar Title", "Tovar Cost", "Store Amount"])
    excel_file_path = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'store.xlsx')
    if os.path.isfile(excel_file_path):
        os.remove(excel_file_path)  # delete the file if it exists
    df.to_excel(excel_file_path, index=False)
    return render_template("store.html", products=results)

# @userApp.route('/excel_store', methods=('GET', 'POST'))
# @login_required
# def excel_store():
#     # if form.validate_on_submit():
#     #     path = request.form['path']  # получаем путь к файлу от пользователя
#         results = db.session.execute(
#             select(Tovar.title, Tovar.cost, Store.amount).join(Store, Tovar.store_id == Store.id)).fetchall()  # получаем данные из базы данных
#         df = pd.DataFrame(results, columns=['Title', 'Cost', 'Amount'])  # создаем DataFrame из данных
#         resp = make_response_from_array(df.to_records(index=False), 'xlsx')  # создаем Excel-файл из DataFrame
#         resp.headers["Content-Disposition"] = f"attachment; filename={path}"  # задаем имя файла и способ загрузки
#         # return resp  # возвращаем пользователю загруженный файл
#     return render_template("excel_store.html")


# @userApp.route('/select_directory', methods=['GET', 'POST'])
# def select_directory():
#     if request.method == 'POST':
#         # root = tk.Tk()
#         # root.withdraw()
#         # file_path = request.files['dir']
#         # path = filedialog.askdirectory()
#         # Use the directory_path variable here to do whatever you want with the selected directory
#         results = db.session.execute(
#             select(Tovar.title, Tovar.cost, Store.amount).join(Store,
#                                                                Tovar.store_id == Store.id)).fetchall()  # получаем данные из базы данных
#         df = pd.DataFrame(results, columns=['Title', 'Cost', 'Amount'])  # создаем DataFrame из данных
#         file_name = 'store.xlsx'
#         file_path = os.path.join(path, file_name)
#         df.to_excel(file_path, index=False)
#         # return f"Selected directory: {directory_path}"
#     else:
#         return render_template('excel_store.html')

# @userApp.route('/form')
# def download_form():
#     return render_template('download.html')

# @userApp.route('/download', methods=['POST'])
# def download():
#     file = request.files['file']  # получаем путь к файлу от пользователя
#     results = db.session.execute(
#         select(Tovar.title, Tovar.cost, Store.amount).join(Store, Tovar.store_id == Store.id)).fetchall()  # получаем данные из базы данных
#     df = pd.DataFrame(results, columns=['Title', 'Cost', 'Amount'])  # создаем DataFrame из данных
#     resp = make_response_from_array(df.to_records(index=False), 'xlsx')  # создаем Excel-файл из DataFrame
#     resp.headers["Content-Disposition"] = f"attachment; filename={path}"  # задаем имя файла и способ загрузки
#     return resp


@userApp.route('/sum_customers', methods=('GET', 'POST'))
@login_required
def sum_customers():
    results = (
        db.session.query(Customer.name, Customer.surname, func.sum(Order.total_value).label('Total_value'))
            .join(Order, Customer.id == Order.customer_id)
            .group_by(Customer.id)
    )

    customers = results.all()
    return render_template("sum_customers.html", customers=customers)


@userApp.route('/excel_sum_customers', methods=('GET', 'POST'))
@login_required
def excel_sum_customers():
    results = (
        db.session.query(Customer.name, Customer.surname, func.sum(Order.total_value).label('Total_value'))
            .join(Order, Customer.id == Order.customer_id)
            .group_by(Customer.id)
    )
    customers = results.all()
    df = pd.DataFrame(customers, columns=["Customer Name", "Customer Surname", "Sum TotalValues"])
    excel_file_path = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'sum_customers.xlsx')
    if os.path.isfile(excel_file_path):
        os.remove(excel_file_path)  # delete the file if it exists
    df.to_excel(excel_file_path, index=False)
    return render_template("sum_customers.html", customers=customers)


@userApp.route('/top_customers', methods=('GET', 'POST'))
@login_required
def top_customers():
    results = (
        db.session.query(
            Customer.name, Customer.surname, func.count(Order.id).label("order_count")
        )
            .join(Order, Customer.id == Order.customer_id)
            .group_by(Customer.id)
            .having(func.count(Order.id) > 0)
            .order_by(func.count(Order.id).desc())
            .limit(5)
    )
    customers = results.all()
    return render_template("top_customers.html", customers=customers)


@userApp.route('/excel_top_customers', methods=('GET', 'POST'))
@login_required
def excel_top_customers():
    results = (
        db.session.query(
            Customer.name, Customer.surname, func.count(Order.id).label("order_count")
        )
            .join(Order, Customer.id == Order.customer_id)
            .group_by(Customer.id)
            .having(func.count(Order.id) > 0)
            .order_by(func.count(Order.id).desc())
            .limit(5)
    )
    customers = results.all()
    df = pd.DataFrame(customers, columns=["Customer Name", "Customer Surname", "Count Orders"])
    excel_file_path = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'top_customers.xlsx')
    if os.path.isfile(excel_file_path):
        os.remove(excel_file_path)  # delete the file if it exists
    df.to_excel(excel_file_path, index=False)
    return render_template("top_customers.html", customers=customers)


@userApp.route('/top_tovar', methods=('GET', 'POST'))
@login_required
def top_tovar():
    from sqlalchemy import func

    results = select(Tovar.title, func.count(func.distinct(OrderTovar.order_id)).label('num_orders')).join(OrderTovar, Tovar.id == OrderTovar.tovar_id).group_by(Tovar.title).order_by(func.count(func.distinct(OrderTovar.order_id)).desc()).limit(1)
    tovars = db.session.execute(results).fetchall()
    return render_template("top_tovar.html", tovars=tovars)


@userApp.route('/excel_top_tovar', methods=('GET', 'POST'))
@login_required
def excel_top_tovar():
    results = select(Tovar.title, func.count(func.distinct(OrderTovar.order_id)).label('num_orders')).join(OrderTovar, Tovar.id == OrderTovar.tovar_id).group_by(
        Tovar.title).order_by(func.count(func.distinct(OrderTovar.order_id)).desc()).limit(1)
    tovars = db.session.execute(results).fetchall()
    df = pd.DataFrame(tovars, columns=["Tovar Title", "Count Orders"])
    excel_file_path = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'top_tovar.xlsx')
    if os.path.isfile(excel_file_path):
        os.remove(excel_file_path)  # delete the file if it exists
    df.to_excel(excel_file_path, index=False)
    return render_template("top_tovar.html", tovars=tovars)


# @userApp.route('/animal/create', methods=['GET', 'POST'])
# @login_required
# def create_animal():
#     form = AnimalForm()
#     if form.validate_on_submit():
#         new_animal = Animal(specie=form.specie.data)
#         db.session.add(new_animal)
#         db.session.commit()
#         return redirect(url_for('read_animals'))
#     return render_template('create_animal.html', form=form, action='Create')


# @userApp.route('/animals')
# @login_required
# def read_animals():
#     animals = Animal.query.all()
#     return render_template('read_animals.html', animals=animals)


# @userApp.route('/animal/<int:id>/update', methods=['GET', 'POST'])
# @login_required
# def edit_animal(id):
#     animal = db.session.query(Animal).get(id)
#     form = AnimalForm(obj=animal)
#     if form.validate_on_submit():
#         form.populate_obj(animal)
#         db.session.commit()
#         return redirect('/animals')
#     return render_template('create_animal.html', form=form, action='Edit')

@userApp.route('/animals', methods=['GET', 'POST', 'PUT', 'DELETE'])
# @login_required
def read_animals():
    data = request.get_json()
    if request.method == "DELETE":
        animal = db.session.query(Animal).get(data["id"])
        # animal = Animal.query.get(id)
        db.session.delete(animal)
        db.session.commit()
        print(data)
    elif request.method == "PUT":
        animal = db.session.query(Animal).get(data["id"])
        animal.specie = data["specie"]
        db.session.commit()
    elif request.method == "POST":
        new_animal = Animal(specie=data["specie"])
        db.session.add(new_animal)
        db.session.commit()
    return render_template('animals.html')

@userApp.route('/animals/search', methods=['POST'])
# @login_required
def animal_search():
    specie = request.get_json()
    if not specie:
        animals = Animal.query.all()
    else:
        animals = list(Animal.query.where(Animal.specie.like(specie + '%')))
    return json.dumps(animals, cls=AnimalEncoder)

class AnimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Animal):
            return {"id": obj.id,
                    "specie": obj.specie}
        # return json.JSONEncoder.default(self, obj)

# @userApp.route('/animal/<int:id>/delete', methods=['POST', 'GET'])
# @login_required
# def delete_animal(id):
#     animal = db.session.query(Animal).get(id)
#     # animal = Animal.query.get(id)
#     db.session.delete(animal)
#     db.session.commit()
#     return redirect('/animals')

class CategoryEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Category):
            return {"id": obj.id,
                    "title": obj.title,
                    "animal_id": obj.animal.id,
                    "animal_specie": obj.animal.specie}


@userApp.route('/categories/search', methods=['POST'])
# @login_required
def category_search():
    title = request.get_json()
    if not title:
        categories = Category.query.all()
    else:
        categories = list(Category.query.where(Category.title.like(title + '%')))
    return json.dumps(categories, cls=CategoryEncoder)

@userApp.route('/categories',  methods=['GET', 'POST', 'PUT', 'DELETE'])
# @login_required
def categories():
    data = request.get_json()
    print(data)
    if data:
        if request.method == "DELETE":
            category = db.session.query(Category).get(data["id"])
            # animal = Animal.query.get(id)
            db.session.delete(category)
            db.session.commit()

        elif request.method == "PUT":
            category = db.session.query(Category).get(data["id"])
            category.title = data["title"]
            category.animal_id = data["animal_id"]
            db.session.commit()
        elif request.method == "POST":
            category = Category(title=data["title"], animal_id=data["animal_id"])
            db.session.add(category)
            db.session.commit()
    return render_template('categories.html')


class TovarEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Tovar):
            return {"id": obj.id,
                    "title": obj.title,
                    "cost": obj.cost,
                    "category_id": obj.category.id,
                    "category_title": obj.category.title,
                    "animal_id": obj.category.animal.id,
                    "animal_specie": obj.category.animal.specie
                    }


@userApp.route('/tovars/search', methods=['POST'])
# @login_required
def tovar_search():
    title = request.get_json()
    if not title:
        tovars = Tovar.query.all()
    else:
        tovars = list(Tovar.query.where(Tovar.title.like(title + '%')))
    return json.dumps(tovars, cls=TovarEncoder)


@userApp.route('/tovars',  methods=['GET', 'POST', 'PUT', 'DELETE'])
# @login_required
def tovars():
    data = request.get_json()
    print(data)
    if data:
        if request.method == "DELETE":
            tovar = db.session.query(Tovar).get(data["id"])
            # animal = Animal.query.get(id)
            db.session.delete(tovar)
            db.session.commit()

        elif request.method == "PUT":
            tovar = db.session.query(Tovar).get(data["id"])
            tovar.title = data["title"]
            tovar.cost = data["cost"]
            tovar.category_id = data["category_id"]
            db.session.commit()
        elif request.method == "POST":
            tovar = Tovar(title=data["title"], cost=data["cost"], category_id=data["category_id"])
            store = Store(
                amount=0,
            )
            db.session.add(tovar)
            db.session.commit()
    return render_template('tovars.html')


class CustomerEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Customer):
            return {"id": obj.id,
                    "surname": obj.surname,
                    "name": obj.name,
                    "lastname": obj.lastname,
                    "fullname": obj.surname + ' ' + obj.name,
                    "discount": obj.discount,
                    "birthday": str(obj.birthday)}


@userApp.route('/customers/search', methods=['POST'])
# @login_required
def customer_search():
    surname = request.get_json()
    if not surname:
        customers = Customer.query.all()
    else:
        customers = list(Customer.query.where(Customer.surname.like(surname + '%')))
    return json.dumps(customers, cls=CustomerEncoder)


@userApp.route('/customers',  methods=['GET', 'POST', 'PUT', 'DELETE'])
# @login_required
def customers():
    data = request.get_json()
    print(data)
    if data:
        if request.method == "DELETE":
            customer = db.session.query(Customer).get(data["id"])
            # animal = Animal.query.get(id)
            db.session.delete(customer)
            db.session.commit()

        elif request.method == "PUT":
            customer = db.session.query(Customer).get(data["id"])
            customer.name = data["name"]
            customer.surname = data["surname"]
            customer.lastname = data["lastname"]
            customer.birthday = data["birthday"]
            db.session.commit()
        elif request.method == "POST":
            customer = Customer(name=data["name"], surname=data["surname"], lastname=data["lastname"], birthday=data["birthday"], discount=0)
            db.session.add(customer)
            db.session.commit()
    return render_template('customers.html')


class ManagerEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Manager):
            return {"id": obj.id,
                    "surname": obj.surname,
                    "name": obj.name,
                    "lastname": obj.lastname,
                    "telethon": obj.telethon,
                    "birthday": str(obj.birthday)}


@userApp.route('/manager/search', methods=['POST'])
# @login_required
def manager_search():
    surname = request.get_json()
    if not surname:
        managers = Manager.query.all()
    else:
        managers = list(Manager.query.where(Manager.surname.like(surname + '%')))
    return json.dumps(managers, cls=ManagerEncoder)


@userApp.route('/managers',  methods=['GET', 'POST', 'PUT', 'DELETE'])
# @login_required
def managers():
    data = request.get_json()
    print(data)
    if data:
        if request.method == "DELETE":
            manager = db.session.query(Manager).get(data["id"])
            # animal = Animal.query.get(id)
            db.session.delete(manager)
            db.session.commit()

        elif request.method == "PUT":
            manager = db.session.query(Manager).get(data["id"])
            manager.name = data["name"]
            manager.surname = data["surname"]
            manager.lastname = data["lastname"]
            manager.birthday = data["birthday"]
            manager.telethon = data["telethon"]
            db.session.commit()
        elif request.method == "POST":
            manager = Manager(name=data["name"], surname=data["surname"], lastname=data["lastname"], birthday=data["birthday"], telethon=data["telethon"])
            db.session.add(manager)
            db.session.commit()
    return render_template('managers.html')


@userApp.route('/providers', methods=['GET', 'POST', 'PUT', 'DELETE'])
# @login_required
def providers():
    data = request.get_json()
    if request.method == "DELETE":
        provider = db.session.query(Provider).get(data["id"])
        # animal = Animal.query.get(id)
        db.session.delete(provider)
        db.session.commit()
        print(data)
    elif request.method == "PUT":
        provider = db.session.query(Provider).get(data["id"])
        provider.title = data["title"]
        provider.telethon = data["telethon"]
        db.session.commit()
    elif request.method == "POST":
        provider = Provider(title=data["title"], telethon = data["telethon"])
        db.session.add(provider)
        db.session.commit()
    return render_template('providers.html')


@userApp.route('/providers/search', methods=['POST'])
# @login_required
def provider_search():
    title = request.get_json()
    if not title:
        providers = Provider.query.all()
    else:
        providers = list(Provider.query.where(Provider.title.like(title + '%')))
    return json.dumps(providers, cls=ProviderEncoder)


class ProviderEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Provider):
            return {"id": obj.id,
                    "title": obj.title,
                    "telethon": obj.telethon}
        # return json.JSONEncoder.default(self, obj)


@userApp.route('/supplies/search', methods=['POST'])
# @login_required
def supply_search():
    supply_number = request.get_json()
    if not supply_number:
        supplies = Supply.query.all()
    else:
        supplies = list(Supply.query.where(Supply.supply_number == supply_number))
    return json.dumps(supplies, cls=SupplyEncoder)


class AmountEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, SupplyTovar):
            return {"title": obj.tovar.title,
                    "tovar_id": obj.tovar_id,
                    "amount": obj.amount}


@userApp.route('/supplies/amounts', methods=['POST'])
# @login_required
def supply_amount():
    supply_id = request.get_json()
    amounts = list(SupplyTovar.query.where(SupplyTovar.supply_id == supply_id))
    return json.dumps(amounts, cls=AmountEncoder)


@userApp.route('/supplies', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def supplies():
    data = request.get_json()
    print(data)
    if request.method == "DELETE":
        supply = db.session.query(Supply).get(data['id'])
        for item in supply.tovars:
            item.tovar.store.amount -= item.amount
        db.session.delete(supply)
        db.session.commit()
    elif request.method == "PUT":
        # provider = db.session.query(Provider).get(data["id"])
        # provider.title = data["title"]
        # provider.telethon = data["telethon"]
        # db.session.commit()
        supply = db.session.query(Supply).get(data['id'])
        supply.supply_number = data['supply_number']
        supply.created_date = data['created_date']
        supply.provider_id = data['provider_id']
        for_remove = []
        for item in supply.tovars:
            item.tovar.store.amount -= item.amount
            for_remove.append(item)
        for item in for_remove:
            supply.tovars.remove(item)
        for i in data['tovars']:
            tovar_id = i['tovar_id']
            title = i['title']
            amount = i['amount']
            product = db.session.query(Tovar).filter_by(id=tovar_id).first()
            suptov = SupplyTovar(amount=amount)
            suptov.tovar = product
            suptov.supply = supply
            product.store.amount += int(amount)
            supply.tovars.append(suptov)
        db.session.commit()

    elif request.method == "POST":
        supply = Supply(supply_number=data['supply_number'], created_date=data['created_date'],
                        provider_id=data['provider_id'], manager_id=current_user.manager_id)
        for i in data['tovars']:
            tovar_id = i['tovar_id']
            title = i['title']
            amount = i['amount']
            product = db.session.query(Tovar).filter_by(id=tovar_id).first()
            # product = db.session.query(Tovar).get(id[0])
            suptov = SupplyTovar(amount=amount)
            suptov.tovar = product
            suptov.supply = supply
            product.store.amount += int(amount)
            supply.tovars.append(suptov)
        db.session.add(supply)
        db.session.commit()
    return render_template('supplies.html')


class SupplyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Supply):
            res = {"id": obj.id,
                        "supply_number": obj.supply_number,
                        "created_date": str(obj.created_date),
                        "provider_id": obj.provider_id,
                        "provider": '',
                        "manager_id": obj.manager_id,
                        "manager": '',
                        "tovars": []}
            if obj.provider:
                res['provider'] = obj.provider.title
            if obj.manager:
                res['manager'] = str(obj.manager.name + ' '+ obj.manager.surname)
            if obj.tovars:
                res['tovars'] = list(i.tovar.title + '\n' for i in obj.tovars)
            return res


@userApp.route('/orders/search', methods=['POST'])
# @login_required
def order_search():
    order_number = request.get_json()
    if not order_number:
        orders = Order.query.all()
    else:
        orders = list(Order.query.where(Order.order_number == order_number))
    return json.dumps(orders, cls=OrderEncoder)


class AmountOrderEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, OrderTovar):
            return {"title": obj.tovar.title,
                    "tovar_id": obj.tovar_id,
                    "amount": obj.amount}


@userApp.route('/orders/amounts', methods=['POST'])
# @login_required
def order_amount():
    order_id = request.get_json()
    amounts = list(OrderTovar.query.where(OrderTovar.order_id == order_id))
    return json.dumps(amounts, cls=AmountOrderEncoder)


@userApp.route('/orders', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def orders():
    data = request.get_json()
    print(data)
    if request.method == "DELETE":
        order = db.session.query(Order).get(data['id'])
        for item in order.tovars:
            item.tovar.store.amount += item.amount
        db.session.delete(order)
        db.session.commit()
    elif request.method == "PUT":
        # provider = db.session.query(Provider).get(data["id"])
        # provider.title = data["title"]
        # provider.telethon = data["telethon"]
        # db.session.commit()
        order = db.session.query(Order).get(data['id'])
        order.order_number = data['order_number']
        order.created_date = data['created_date']
        order.customer_id = data['customer_id']
        for_remove = []
        for item in order.tovars:
            item.tovar.store.amount += item.amount
            for_remove.append(item)
        for item in for_remove:
            order.tovars.remove(item)
        for i in data['tovars']:
            tovar_id = i['tovar_id']
            title = i['title']
            amount = i['amount']
            product = db.session.query(Tovar).filter_by(id=tovar_id).first()
            suptov = OrderTovar(amount=amount)
            suptov.tovar = product
            suptov.order = order
            product.store.amount -= int(amount)
            order.tovars.append(suptov)
        db.session.commit()

    elif request.method == "POST":
        order = Order(order_number=data['supply_number'], created_date=data['created_date'],
                        customer_id=data['customer_id'], manager_id=current_user.manager_id)
        summ = 0
        for i in data['tovars']:
            tovar_id = i['tovar_id']
            title = i['title']
            amount = i['amount']
            product = db.session.query(Tovar).filter_by(id=tovar_id).first()
            # product = db.session.query(Tovar).get(id[0])
            suptov = OrderTovar(amount=amount)
            suptov.tovar = product
            suptov.order = order
            product.store.amount -= int(amount)
            summ += int(amount) * product.cost
            order.tovars.append(suptov)
        order.total_value = summ * (100 - order.customer.discount) // 100
        if (summ > 500):
            order.customer.discount += 1 % 50

        db.session.add(order)
        db.session.commit()
    return render_template('orders.html')


class OrderEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Order):
            res = {"id": obj.id,
                        "order_number": obj.order_number,
                        "created_date": str(obj.created_date),
                        "customer_id": obj.customer_id,
                        "customer": '',
                        "manager_id": obj.manager_id,
                        "manager": '',
                        "tovars": []}
            if obj.customer:
                res['customer'] = str(obj.customer.name + ' '+ obj.customer.surname)
            if obj.manager:
                res['manager'] = str(obj.manager.name + ' '+ obj.manager.surname)
            if obj.tovars:
                res['tovars'] = list(i.tovar.title + '\n' for i in obj.tovars)
            return res

@userApp.route('/category/create', methods=['GET', 'POST'])
@login_required
def create_category():
    form = CategoryForm(animal_choices=Animal.query.all())
    # form.animal.choices = [(animal.id, animal.specie) for animal in Animal.query.all()]
    if form.validate_on_submit():
        category = Category(
            title=form.title.data,
            animal_id=form.animal.data
        )
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('categories'))
    return render_template('create_category.html', form=form, action='Create')


@userApp.route('/category/<int:id>/update', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    category = db.session.query(Category).get(id)
    form = CategoryForm(animal_choices=Animal.query.all(), obj=category)
    if form.validate_on_submit():
        category.title = form.title.data
        category.animal_id = form.animal.data
        # form.populate_obj(category)
        db.session.commit()
        return redirect(url_for('categories'))
    return render_template('create_category.html', form=form, action='Update')


@userApp.route('/category/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_category(id):
    category = db.session.query(Category).get(id)
    db.session.delete(category)
    db.session.commit()
    return redirect('/categories')


# @userApp.route('/tovars')
# @login_required
# def tovars():
#     tovars = Tovar.query.all()
#     return render_template('read_tovars.html', tovars=tovars)


@userApp.route('/tovar/create', methods=['GET', 'POST'])
@login_required
def create_tovar():
    form = TovarForm(category_choices=Category.query.all())
    if form.validate_on_submit():
        # создаем новый товар
        store = Store(
            amount=0,
        )
        tovar = Tovar(
            title=form.title.data,
            cost=form.cost.data,
            store=store,
            category_id=form.category.data
        )

        db.session.add(tovar)
        db.session.commit()
        return redirect('/tovars')
    return render_template('create_tovar.html', action='Create', form=form)


@userApp.route('/tovar/<int:id>/update', methods=['GET', 'POST'])
@login_required
def edit_tovar(id):
    tovar = db.session.query(Tovar).get(id)
    form = TovarForm(category_choices=Category.query.all(), obj=tovar)
    if form.validate_on_submit():
        tovar.title = form.title.data
        tovar.cost = form.cost.data
        tovar.category_id = form.category.data
        db.session.commit()
        return redirect('/tovars')
    return render_template('create_tovar.html', title='Edit', form=form)


@userApp.route('/tovar/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_tovar(id):
    tovar = db.session.query(Tovar).get(id)
    db.session.delete(tovar)
    db.session.commit()
    return redirect('/tovars')
#
# @userApp.route('/providers')
# @login_required
# def providers():
#     providers = Provider.query.all()
#     return render_template('read_providers.html', providers=providers)


@userApp.route('/provider/create', methods=['GET', 'POST'])
@login_required
# @login_required
def create_provider():
    form = ProviderForm()
    if form.validate_on_submit():
        provider = Provider(title=form.title.data, telethon=form.telethon.data)
        db.session.add(provider)
        db.session.commit()
        return redirect(url_for('providers'))
    return render_template('create_provider.html', action='Create', form=form)


@userApp.route('/provider/<int:id>/update', methods=['GET', 'POST'])
@login_required
def edit_provider(id):
    provider = db.session.query(Provider).get(id)
    form = ProviderForm(obj=provider)
    if form.validate_on_submit():
        form.populate_obj(provider)
        db.session.commit()
        return redirect('/providers')
    return render_template('create_provider.html', form=form, action='Edit')


@userApp.route('/provider/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_provider(id):
    provider = db.session.query(Provider).get(id)
    db.session.delete(provider)
    db.session.commit()
    return redirect(url_for('providers'))


# @userApp.route('/managers')
# @login_required
# def managers():
#     managers = Manager.query.all()
#     return render_template('read_managers.html', managers=managers)


@userApp.route('/manager/create', methods=['GET', 'POST'])
@login_required
# @login_required
def create_manager():
    form = ManagerForm()
    if form.validate_on_submit():
        new_manager = Manager(name=form.name.data,
                              surname=form.surname.data,
                              lastname=form.lastname.data,
                              telethon=form.telethon.data,
                              birthday=form.birthday.data)
        db.session.add(new_manager)
        db.session.commit()
        return redirect(url_for('managers'))
    return render_template('create_manager.html', form=form, action='Create')


@userApp.route('/manager/<int:id>/update', methods=['GET', 'POST'])
@login_required
def edit_manager(id):
    manager = db.session.query(Manager).get(id)
    form = ManagerForm(obj=manager)
    if form.validate_on_submit():
        form.populate_obj(manager)
        db.session.commit()
        return redirect('/managers')
    return render_template('create_manager.html', form=form, action='Edit')


@userApp.route('/manager/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_manager(id):
    manager = db.session.query(Manager).get(id)
    db.session.delete(manager)
    db.session.commit()
    return redirect(url_for('managers'))


# @userApp.route('/customers')
# @login_required
# def customers():
#     customers = Customer.query.all()
#     return render_template('read_customers.html', customers=customers)


@userApp.route('/customer/create', methods=['GET', 'POST'])
@login_required
# @login_required
def create_customer():
    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customer(name=form.name.data,
                              surname=form.surname.data,
                              lastname=form.lastname.data,
                              discount=0,
                              birthday=form.birthday.data)
        db.session.add(customer)
        db.session.commit()
        return redirect(url_for('customers'))
    return render_template('create_customer.html', form=form, action='Create')


@userApp.route('/customer/<int:id>/update', methods=['GET', 'POST'])
@login_required
def edit_customer(id):
    customer = db.session.query(Customer).get(id)
    form = CustomerForm(obj=customer)
    if form.validate_on_submit():
        form.populate_obj(customer)
        db.session.commit()
        return redirect(url_for('customers'))
    return render_template('create_customer.html', form=form, action='Edit')


@userApp.route('/customer/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_customer(id):
    customer = db.session.query(Customer).get(id)
    db.session.delete(customer)
    db.session.commit()
    return redirect(url_for('customers'))


# @userApp.route('/supplies')
# @login_required
# def supplies():
#     supplies = Supply.query.all()
#     return render_template('read_supplies.html', supplies=supplies)


@userApp.route('/supply/<int:id>/update', methods=['GET', 'POST'])
@login_required
def edit_supply(id):
    supply = db.session.query(Supply).get(id)
    products = []
    for item in supply.tovars:
        products.append(item.tovar)
    tovars_choices = [(tovar.id, str(tovar.title + " " + tovar.category.title + " " + tovar.category.animal.specie)) for
                      tovar in products]
    # print(tovars_choices)
    form = SupplyForm(provider_choices=Provider.query.all(), manager_choices=Manager.query.all(), obj=supply)
    if (not form.tovars):
        for i in range(len(tovars_choices)):
            form.tovars.append_entry()
            form.hidden_tag()
    if form.validate_on_submit():
        supply.supply_number = form.supply_number.data
        supply.created_date = form.created_date.data
        supply.provider_id = form.provider.data
        supply.manager_id = form.manager.data
        for_remove = []
        for i, id, item in zip(form.tovars.entries, tovars_choices, supply.tovars):
            item.tovar.store.amount -= item.amount
            if i.form.tovar.data == True:
                item.amount = i.form.amount.data
                item.tovar.store.amount += i.form.amount.data
            else:
                for_remove.append(item)
        for item in for_remove:
            supply.tovars.remove(item)
        db.session.commit()
        return redirect(url_for('supplies'))
    else:
        print(form.errors)
    return render_template('create_supply.html', form=form, action="Update", products=tovars_choices)


@userApp.route('/create_supply', methods=['GET', 'POST'])
@login_required
def create_supply():
    tovars_choices = [(tovar.id, str(tovar.title + " " + tovar.category.title + " " + tovar.category.animal.specie)) for
                      tovar in Tovar.query.all()]
    form = SupplyForm(provider_choices=Provider.query.all(), manager_choices=Manager.query.all(), tovar_choices=Tovar.query.all())
    if (not form.tovars):
        for i in range(len(tovars_choices)):
            form.tovars.append_entry()
            form.hidden_tag()
            # print(i)
    if form.validate_on_submit():
        supply = Supply(supply_number=form.supply_number.data, created_date=form.created_date.data,
                        provider_id=form.provider.data, manager_id=form.manager.data)

        # selected_tovars = MultiDict(request.form).getlist('tovars')
        # print(selected_tovars)
        for i, id in zip(form.tovars.entries, tovars_choices):
            if i.form.tovar.data == True:
                product = db.session.query(Tovar).filter_by(id=id[0]).first()
                # product = db.session.query(Tovar).get(id[0])
                suptov = SupplyTovar(amount=i.form.amount.data)
                suptov.tovar = product
                suptov.supply = supply
                product.store.amount += i.form.amount.data
                supply.tovars.append(suptov)
            print(i.form.amount.data, i.form.tovar.data, id)
        # amounts = {}
        # for tovar in tovars:
        #     amount = request.form.get('amount_{}'.format(tovar.id))
        #     if amount is not None:
        #         amounts[tovar.id] = int(amount)
        # print(amounts)
        # for tovar_id, tov, amount in zip(tovars_choices, form.tovars.tovar.data, form.tovars.amount.data):
        #     print(tovar_id, tov, amount)
        db.session.add(supply)
        db.session.commit()
        return redirect(url_for('supplies'))
    else:
        print(form.errors)
    return render_template('create_supply.html', form=form, action="Create", products=tovars_choices)


@userApp.route('/supply/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_supply(id):
    supply = db.session.query(Supply).get(id)
    for item in supply.tovars:
        item.tovar.store.amount -= item.amount
    #     # item.tovar.supplies.remove(item)
    #     supply.tovars.remove(item)

        # db.session.flash()
    db.session.delete(supply)
    db.session.commit()
    return redirect(url_for('supplies'))


# @userApp.route('/orders')
# @login_required
# def orders():
#     orders = Order.query.all()
#     return render_template('read_orders.html', orders=orders)


@userApp.route('/order/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_order(id):
    order = db.session.query(Order).get(id)
    for item in order.tovars:
        item.tovar.store.amount += item.amount
    #     # item.tovar.supplies.remove(item)
    #     supply.tovars.remove(item)

        # db.session.flash()
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for('orders'))


@userApp.route('/order/<int:id>/update', methods=['GET', 'POST'])
@login_required
def edit_order(id):
    order = db.session.query(Order).get(id)
    products = []
    for item in order.tovars:
        products.append(item.tovar)
    # products = Tovar.query.all()
    tovars_choices = [(tovar.id, str(tovar.title + " " + tovar.category.title + " " + tovar.category.animal.specie)) for
                      tovar in products]
    form = OrderForm(customer_choices=Customer.query.all(), manager_choices=Manager.query.all(), obj=order)
    if (not form.tovars):
        for i in range(len(tovars_choices)):
            form.tovars.append_entry()
            form.hidden_tag()
    if form.validate_on_submit():
        order.order_number = form.order_number.data
        order.created_date = form.created_date.data
        order.customer_id = form.customer.data
        order.manager_id = form.manager.data
        for_remove = []
        for i, id, item in zip(form.tovars.entries, tovars_choices, order.tovars):
            item.tovar.store.amount += item.amount
            if i.form.tovar.data == True:
                item.amount = i.form.amount.data
                item.tovar.store.amount -= i.form.amount.data
            else:
                for_remove.append(item)
        for item in for_remove:
            order.tovars.remove(item)
        db.session.commit()
        return redirect(url_for('orders'))
    else:
        print(form.errors)
    return render_template('create_order.html', form=form, action="Update", products=tovars_choices)


@userApp.route('/create_order', methods=['GET', 'POST'])
@login_required
def create_order():
    tovars_choices = [(tovar.id, str(tovar.title + " - " + tovar.category.title + " - " + tovar.category.animal.specie +
                                    " - " + str(tovar.cost))) for tovar in Tovar.query.all()]
    form = OrderForm(customer_choices=Customer.query.all(), manager_choices=Manager.query.all())
    if (not form.tovars):
        for i in range(len(tovars_choices)):
            form.tovars.append_entry()
            form.hidden_tag()
    if form.validate_on_submit():
        order = Order(order_number=form.order_number.data, created_date=form.created_date.data,
                        customer_id=form.customer.data, manager_id=form.manager.data)
        summ = 0
        for i, id in zip(form.tovars.entries, tovars_choices):
            if i.form.tovar.data == True:
                product = db.session.query(Tovar).filter_by(id=id[0]).first()
                ordtov = OrderTovar(amount=i.form.amount.data)
                ordtov.tovar = product
                ordtov.order = order
                product.store.amount -= i.form.amount.data
                summ += i.form.amount.data * product.cost
                order.tovars.append(ordtov)
            print(i.form.amount.data, i.form.tovar.data, id)
        order.total_value = summ * (100 - order.customer.discount) // 100
        if (summ > 500):
            order.customer.discount += 1 % 50
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('orders'))
    else:
        print(form.errors)
    return render_template('create_order.html', form=form, action="Create", products=tovars_choices)





if __name__ == "__main__":
    userApp.run(debug=True,  port=8080)