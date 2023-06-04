# -*- coding: utf-8 -*-
import flask
from config import config
from flask_bootstrap import Bootstrap
import os
from flask_sqlalchemy import SQLAlchemy
userApp = flask.Flask(__name__)
bootstrap = Bootstrap(userApp)
userApp.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE']['URI']
userApp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# Создание сессии для БД
db = SQLAlchemy(userApp)
# Инициализация классов БД
from userApp.database import *
# Создание таблиц БД в соответствии с описанными классами
db.create_all()
userApp.config['SECRET_KEY'] = os.environ.get("SECRET_KEY") or os.urandom(24)

