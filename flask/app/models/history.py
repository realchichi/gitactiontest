from app import db
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime , timezone

class History(db.Model, SerializerMixin):
	__tablename__ = "histories"

	id = db.Column(db.Integer, primary_key=True)
	plant_id = db.Column(db.Integer, db.ForeignKey('plant_info.id'))
	account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
	idendtfied_date = db.Column(db.DateTime)
	idendtfied_img = db.Column(db.String(100))
	is_removed = db.Column(db.Boolean(), default=False)
	removed_date = db.Column(db.DateTime)
	removed_by = db.Column(db.String(100))
	def __init__(self, plant_id, account_id, idendtfied_date, idendtfied_img):
		self.plant_id = plant_id
		self.account_id = account_id
		self.idendtfied_date = datetime.now(timezone.utc)
		self.idendtfied_img = idendtfied_img


	def remove_history(self, account_id):
		self.is_removed = True
		self.removed_date = datetime.now(timezone.utc)
		self.removed_by = account_id