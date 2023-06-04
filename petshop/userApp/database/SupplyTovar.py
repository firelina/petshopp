from userApp import db
from sqlalchemy.orm import relationship

# supply_tovar_table = db.Table('supply_tovar', db.Model.metadata,
#     db.Column('supply_id', db.Integer, db.ForeignKey('supply.id')),
#     db.Column('tovar_id', db.Integer, db.ForeignKey('tovar.id')),
#     db.Column('amount', db.Integer)
# )


class SupplyTovar(db.Model):
    __tablename__ = "supply_tovar"
    supply_id = db.Column(db.Integer, db.ForeignKey("supply.id"),  primary_key=True)
    tovar_id = db.Column(db.Integer, db.ForeignKey("tovar.id"),  primary_key=True)
    amount = db.Column(db.Integer)
    supply = relationship("Supply", back_populates="tovars")
    tovar = relationship("Tovar", back_populates="supplies")
