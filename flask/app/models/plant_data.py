from app import db
from sqlalchemy_serializer import SerializerMixin

class Plant_data(db.Model, SerializerMixin):
	__tablename__ = "plant_data"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	
	def __init__(self, name):
		self.name = name

