from userApp import db
from sqlalchemy.orm import relationship


class Manager(db.Model):
    __tablename__ = "manager"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    lastname = db.Column(db.String)
    telethon = db.Column(db.String)
    birthday = db.Column(db.Date)

    orders = relationship("Order", back_populates="manager")
    user = relationship("User", back_populates="manager")
    supplies = relationship("Supply", back_populates="manager")

    @property
    def serialize(self):
        return {
            'id': self.id,
            'surname': self.surname,
            'name': self.name,
            'lastname': self.lastname,
            'telethon': self.telethon,
            'birthday': self.birthday,
        }