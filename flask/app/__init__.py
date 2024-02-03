from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, static_folder="static")
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True

db = SQLAlchemy(app)



from app import views 