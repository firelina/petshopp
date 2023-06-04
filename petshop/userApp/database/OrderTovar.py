from userApp import db
from sqlalchemy.orm import relationship

class OrderTovar(db.Model):
    __tablename__ = "order_tovar"
    __table_args__ = {'extend_existing': True}
    # id = db.Column(db.Integer, primary_key=True)
    tovar_id = db.Column(db.Integer, db.ForeignKey("tovar.id"), primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), primary_key=True)
    amount = db.Column(db.Integer)
    order = relationship("Order", back_populates="tovars")
    tovar = relationship("Tovar", back_populates="orders")


    @property
    def serialize(self):
        return {
            'amount': self.title
        }