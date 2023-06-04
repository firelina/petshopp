from userApp import db
from sqlalchemy.orm import relationship

# order_tovar_table = db.Table('order_tovar', db.Model.metadata,
#     db.Column('order_id', db.Integer, db.ForeignKey('order.id')),
#     db.Column('tovar_id', db.Integer, db.ForeignKey('tovar.id')),
#     db.Column('amount', db.Integer)
# )

class Order(db.Model):
    __tablename__ = "order"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.Integer)
    total_value = db.Column(db.Integer)
    created_date = db.Column(db.Date)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    customer = relationship("Customer", back_populates="orders")
    manager_id = db.Column(db.Integer, db.ForeignKey("manager.id"))
    manager = relationship("Manager", back_populates="orders")
    tovars = relationship('OrderTovar',  back_populates='order', cascade="all, delete-orphan")

    @property
    def serialize(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'total_value': self.total_value,
            'created_date': self.created_date
        }

