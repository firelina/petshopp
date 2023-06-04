from userApp import db
# from userApp.database.Order import order_tovar_table
# from userApp.database.Supply import supply_tovar_table
from sqlalchemy.orm import relationship


# store = db.Table('store', db.Model.metadata,
#     db.Column('tovar_id', db.Integer, db.ForeignKey('tovar.id')),
#     db.Column('amount', db.Integer)
# )

class Tovar(db.Model):
    __tablename__ = "tovar"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    cost = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    category = relationship("Category", back_populates="tovars")
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"))
    store = relationship("Store", back_populates="tovar", uselist=False, cascade="all")
    orders = relationship('OrderTovar', back_populates='tovar')
    supplies = relationship('SupplyTovar', back_populates='tovar')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'cost': self.cost,
            'title': self.title
        }