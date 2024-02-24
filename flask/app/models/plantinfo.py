from app import db
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin

class PlantInfo(db.Model, SerializerMixin):
	__tablename__ = "plant_info"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	url_image = db.Column(db.String(100))
	description = db.Column(db.String(1000))
	wiki_url = db.Column(db.String(200))
	taxonomy = db.Column(db.String(200))
	commom_name = db.Column(db.String(100))
	similar_image = db.Column(db.String(100))
	probability = db.Column(db.Float)
	history_id = db.Column(db.Integer, db.ForeignKey('histories.id'))
	def __init__(self, name, url_image, description, wiki_url, taxonomy, commom_name, similar_image, probability, history_id):
		self.name = name
		self.url_image = url_image
		self.description = description
		self.wiki_url = wiki_url
		self.taxonomy = taxonomy
		self.commom_name = commom_name
		self.similar_image = similar_image
		self.probability = probability
		self.history_id = history_id