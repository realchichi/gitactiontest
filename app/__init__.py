from flask import Flask

from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__, static_folder="static")
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@test:5432/plant_data'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy()
def create_app():
	db.init_app(app)
	return db

app = Flask(__name__, static_folder="static")
app.config['DEBUG'] = True

from app import views 