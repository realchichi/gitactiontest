from app import db
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime , timezone

class Community(db.Model, SerializerMixin):
	__tablename__ = "communities"

	id = db.Column(db.Integer, primary_key=True)
	history_id = db.Column(db.Integer, db.ForeignKey('histories.id'))
	shared_date = db.Column(db.DateTime)
	edited_date = db.Column(db.DateTime)
	removed_date = db.Column(db.DateTime, default=None)
	removed_by = db.Column(db.String(100), default=None)
	message = db.Column(db.String(280))


	def __init__(self, history_id):
		self.history_id = history_id
		self.shared_date = datetime.now(timezone.utc)
		self.edit_date = datetime.now(timezone.utc)


	def edit(self,message):
		self.message = message
		self.edit_date = datetime.now(timezone.utc)


	def remove_history(self, account_id):
		self.removed_date = datetime.now(timezone.utc)
		self.removed_by = account_id


class Comment(db.Model, SerializerMixin):
	__tablename__ = "comment"

	id = db.Column(db.Integer, primary_key=True)
	_id = db.Column(db.Integer, db.ForeignKey('histories.id'))
	comment_date = db.Column(db.DateTime)
	edited_date = db.Column(db.DateTime)
	removed_date = db.Column(db.DateTime)
	removed_by = db.Column(db.String(100))
	message = db.Column(db.String(280))
	def __init__(self, history_id,message):
		self.history_id = history_id
		self.comment_date = datetime.now(timezone.utc)
		self.edit_date = datetime.now(timezone.utc)
		self.message = message
	def edit_comment(self,message):
		self.message = message
		self.edit_date = datetime.now(timezone.utc)

	def remove_comment(self, account_id):
		self.removed_date = datetime.now(timezone.utc)
		self.removed_by = account_id
