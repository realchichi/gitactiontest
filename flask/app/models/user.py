from app import db
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin

# class User(db.Model, SerializerMixin):
# 	__tablename__ = "users"

# 	id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(50))
#     password = db.Column(db.String(50))
    


#     def __init__(self, email, password):
#     	self.email = email
#     	self.password = password


#     def update(self, email, password):
#        	self.email = email
#     	self.password = password
class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(200))
    name = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, email,password,name):
        self.email = email
        self.password = password
        self.name = name

    def update(self, email,password,name):
        self.email = email
        self.password = password
        self.name = name