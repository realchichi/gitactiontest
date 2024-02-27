from app import db
from sqlalchemy_serializer import SerializerMixin


class PlantInfo(db.Model, SerializerMixin):
	__tablename__ = "plant_info"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200))
	url_image = db.Column(db.String(200))
	description = db.Column(db.String(2000))
	wiki_url = db.Column(db.String(200))
	taxonomy = db.Column(db.String(200))
	common_name = db.Column(db.String(200))
	similar_images = db.Column(db.String(300))
	probability = db.Column(db.Float)
	history_id = db.Column(db.Integer, db.ForeignKey('histories.id'))
	def __init__(self, name, url_image, description, wiki_url, taxonomy, common_name, similar_images, probability, history_id):
		self.name = name
		self.url_image = url_image
		self.description = description
		self.wiki_url = wiki_url
		self.taxonomy = taxonomy
		self.common_name = common_name
		self.similar_images = similar_images
		self.probability = probability
		self.history_id = history_id