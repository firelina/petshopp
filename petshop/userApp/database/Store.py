from userApp import db
from sqlalchemy.orm import relationship


class Store(db.Model):
    __tablename__ = "store"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer,  primary_key=True)
    amount = db.Column(db.Integer)
    tovar = relationship("Tovar", back_populates="store")

    @property
    def serialize(self):
        return {
            'amount': self.title
        }