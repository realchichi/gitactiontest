from app import db
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime , timezone

class Commu(db.Model, SerializerMixin):
	__tablename__ = "commu"

	id = db.Column(db.Integer, primary_key=True)
	history_id = db.Column(db.Integer, db.ForeignKey('histories.id'))
	shared_date = db.Column(db.DateTime)
	edited_date = db.Column(db.DateTime)
	removed_date = db.Column(db.DateTime)
	removed_by = db.Column(db.String(100))
	message = db.Column(db.String(280))
	def __init__(self, history_id):
		self.history_id = history_id
		self.identified_date = datetime.now(timezone.utc)
		self.edit_date = datetime.now(timezone.utc)
	def edit(self,message):
		self.message = message
		self.edit_date = datetime.now(timezone.utc)

	def remove_history(self, account_id):
		self.removed_date = datetime.now(timezone.utc)
		self.removed_by = account_id

