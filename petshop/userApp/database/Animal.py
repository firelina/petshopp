from userApp import db
from sqlalchemy.orm import relationship

class Animal(db.Model):
    __tablename__ = "animal"
    id = db.Column(db.Integer, primary_key=True)
    specie = db.Column(db.String)
    categories = relationship("Category", back_populates="animal")

    @property
    def serialize(self):
        return {
            'id': self.id,
            'specie': self.specie
        }