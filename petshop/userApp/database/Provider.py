from userApp import db
from sqlalchemy.orm import relationship

class Provider(db.Model):
    __tablename__ = "provider"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    telethon = db.Column(db.String())
    # user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    supplies = relationship("Supply", back_populates="provider")

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'telethon': self.telethon
        }