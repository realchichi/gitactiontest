from app import db
from sqlalchemy_serializer import SerializerMixin

class User(db.Model, SerializerMixin):
	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    


    def __init__(self, firstname, lastname):
    	self.firstname = firstname
    	self.lastname = lastname


    def update(self, firstname, lastname):
       	self.firstname = firstname
    	self.lastname = lastname