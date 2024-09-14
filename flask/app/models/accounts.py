from app import db
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin



class Account(db.Model, UserMixin,SerializerMixin):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(200))
    name = db.Column(db.String(200))
    avatar_url = db.Column(db.String(100))
    # is_active = db.Column(db.Boolean, default=True)
    value = db.Column(db.Integer)
    login_with = db.Column(db.String(50))

    def __init__(self, email,password,name,avatar_url,login_with):
        self.email = email
        self.password = password
        self.name = name
        self.avatar_url = avatar_url
        self.login_with = login_with
        self.value = 3
    def update(self, email,avatar_url,name,password):
        self.email = email
        self.avatar_url = avatar_url
        self.name = name
        self.password = password
    def re_value(self):
        self.value = 3
    def increse(self):
        self.value = self.value-1