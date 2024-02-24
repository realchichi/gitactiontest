from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, current_user


app = Flask(__name__, static_folder="static")
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '5daa398942861011cebf82daa710fc7b162149e3833156c0'

db = SQLAlchemy(app)



from app import views 