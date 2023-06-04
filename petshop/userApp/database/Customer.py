from userApp import db
from sqlalchemy.orm import relationship


class Customer(db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    lastname = db.Column(db.String)
    discount = db.Column(db.Integer)
    birthday = db.Column(db.Date)
    orders = relationship("Order", back_populates="customer")

    @property
    def serialize(self):
        return {
            'id': self.id,
            'surname': self.surname,
            'name': self.name,
            'lastname': self.lastname,
            'discount': self.discount,
            'birthday': self.birthday,
        }