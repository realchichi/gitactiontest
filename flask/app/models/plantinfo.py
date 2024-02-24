from app import db
from sqlalchemy_serializer import SerializerMixin

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
	def __init__(self, name, url_image, description, wiki_url, taxonomy, commom_name, similar_image):
		self.name = name
		self.url_image = url_image
		self.description = description
		self.wiki_url = wiki_url
		self.taxonomy = taxonomy
		self.commom_name = commom_name
		self.similar_image = similar_image
