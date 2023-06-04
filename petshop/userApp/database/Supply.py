from userApp import db
from sqlalchemy.orm import relationship

# supply_tovar_table = db.Table('supply_tovar', db.Model.metadata,
#     db.Column('supply_id', db.Integer, db.ForeignKey('supply.id')),
#     db.Column('tovar_id', db.Integer, db.ForeignKey('tovar.id')),
#     db.Column('amount', db.Integer)
# )


class Supply(db.Model):
    __tablename__ = "supply"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    supply_number = db.Column(db.Integer)
    created_date = db.Column(db.Date)
    provider_id = db.Column(db.Integer, db.ForeignKey("provider.id"))
    provider = relationship("Provider", back_populates="supplies")
    manager_id = db.Column(db.Integer, db.ForeignKey("manager.id"))
    manager = relationship("Manager", back_populates="supplies")
    tovars = relationship('SupplyTovar', back_populates='supply', cascade="all, delete-orphan")

    @property
    def serialize(self):
        return {
            'id': self.id,
            'supply_number': self.supply_number,
            'created_date': self.created_date,
            'contract_date': self.contract_date
        }