from userApp import db
from sqlalchemy.orm import relationship


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    animal_id = db.Column(db.Integer, db.ForeignKey("animal.id"))
    animal = relationship("Animal", back_populates="categories")
    tovars = relationship("Tovar", back_populates="category")

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title

        }