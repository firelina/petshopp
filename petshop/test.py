from unittest import TestCase

from petshop.userApp.database import Animal
from run import userApp, db
# from yourapp.models import Animal
from config import config
# from petshop.userApp import userApp


class TestCreateAnimal(TestCase):
    def setUp(self):
        userApp.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE']['URI']
        userApp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        userApp.config['TESTING'] = True
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_animal_adds_animal_to_database(self):
        with userApp.test_client() as client:
            with client.session_transaction() as session:
                session['user_id'] = 2
            # отправляем POST-запрос с данными формы для добавления нового животного
            response = client.post('/animal/create', data={
                'specie': 'cat'
            }, follow_redirects=True)
            # проверяем, что статус код 200
            self.assertEqual(response.status_code, 200)
            # проверяем, что животное нового типа добавлено в базу
            self.assertTrue(Animal.query.filter_by(specie='cat').first())
