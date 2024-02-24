from app import db
from sqlalchemy_serializer import SerializerMixin


class Account(db.Model, SerializerMixin):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(200))
    name = db.Column(db.String(200))


    def __init__(self, email,password,name):
        self.email = email
        self.password = password
        self.name = name

    def update(self, email,password,name):
        self.email = email
        self.password = password
        self.name = name