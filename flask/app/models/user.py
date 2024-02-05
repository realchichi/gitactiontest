# from app import db
# from sqlalchemy_serializer import SerializerMixin

# class User(db.Model, SerializerMixin):
# 	__tablename__ = "users"

# 	id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(50))
#     password = db.Column(db.String(50))
    


#     def __init__(self, email, password):
#     	self.email = email
#     	self.password = password


#     def update(self, email, password):
#        	self.email = email
#     	self.password = password