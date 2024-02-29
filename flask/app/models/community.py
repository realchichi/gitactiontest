from app import db
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime , timezone

class Community(db.Model, SerializerMixin):
	__tablename__ = "communities"

	id = db.Column(db.Integer, primary_key=True)
	account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
	shared_date = db.Column(db.DateTime)
	edited_date = db.Column(db.DateTime)
	removed_date = db.Column(db.DateTime, default=None)
	removed_by = db.Column(db.String(100), default=None)
	message = db.Column(db.String(280))
	plant_name = db.Column(db.String(100), default="Undefied")
	img_plant = db.Column(db.String(100))
	def __init__(self, account_id,message,img_plant,plant_name):
		self.account_id = account_id
		self.shared_date = datetime.now(timezone.utc)
		self.edit_date = datetime.now(timezone.utc)
		self.message = message
		self.plant_name = plant_name
		self.img_plant =img_plant
	def edit(self,message):
		self.message = message
		self.edit_date = datetime.now(timezone.utc)


	def remove_history(self, account_id):
		self.removed_date = datetime.now(timezone.utc)
		self.removed_by = account_id


class Comment(db.Model, SerializerMixin):
	__tablename__ = "comment"

	id = db.Column(db.Integer, primary_key=True)
	commu_id = db.Column(db.Integer, db.ForeignKey('communities.id'))
	accout.id = db.Column(db.Integer, db.ForeignKey('account.id'))
	comment_date = db.Column(db.DateTime)
	edited_date = db.Column(db.DateTime)
	removed_date = db.Column(db.DateTime)
	removed_by = db.Column(db.String(100))
	message = db.Column(db.String(280))
	def __init__(self, commu_id,message,account):
		self.commu_id = commu_id
		self.account = account
		self.comment_date = datetime.now(timezone.utc)
		self.edit_date = datetime.now(timezone.utc)
		self.message = message
	def edit_comment(self,message):
		self.message = message
		self.edit_date = datetime.now(timezone.utc)

	def remove_comment(self, account_id):
		self.removed_date = datetime.now(timezone.utc)
		self.removed_by = account_id
