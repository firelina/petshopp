from userApp import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

# класс
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String)
    email = db.Column(db.String)
    hashed_password = db.Column(db.String)
    role = db.Column(db.Boolean)
    manager_id = db.Column(db.Integer, db.ForeignKey("manager.id"), nullable=False)
    manager = relationship("Manager", back_populates="user", uselist=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'login': self.login,
            'email': self.email,
            'password': self.hashed_password,

        }

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)