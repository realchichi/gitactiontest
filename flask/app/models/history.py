from app import db
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime , timezone

class History(db.Model, SerializerMixin):
	__tablename__ = "histories"

	id = db.Column(db.Integer, primary_key=True)
	account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
	idendtfied_date = db.Column(db.DateTime)
	idendtfied_img = db.Column(db.String(100))
	removed_date = db.Column(db.DateTime)
	removed_by = db.Column(db.String(100))
	def __init__(self, account_id, idendtfied_img):
		self.account_id = account_id
		self.identified_date = datetime.now(timezone.utc)
		self.identified_img = idendtfied_img
		self.removed_date = "None"
		self.removed_by = "None"

	def remove_history(self, account_id):
		self.removed_date = datetime.now(timezone.utc)
		self.removed_by = account_id