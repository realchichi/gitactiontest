from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth

app = Flask(__name__, static_folder="static")
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '5daa398942861011cebf82daa710fc7b162149e3833156c0'

app.config['UPLOAD_FOLDER'] = "uploads"


app.config['GOOGLE_CLIENT_ID'] = os.getenv("GOOGLE_CLIENT_ID", None)
app.config['GOOGLE_CLIENT_SECRET'] = os.getenv("GOOGLE_CLIENT_SECRET", None)
app.config['GOOGLE_DISCOVERY_URL'] = os.getenv("GOOGLE_DISCOVERY_URL", None)

app.config['FACEBOOK_CLIENT_ID'] = os.getenv("FACEBOOK_CLIENT_ID", None)
app.config['FACEBOOK_CLIENT_SECRET'] = os.getenv("FACEBOOK_CLIENT_SECRET", None)
# print("........................",os.getenv("FACEBOOK_CLIENT_ID", None),os.getenv("FACEBOOK_CLIENT_SECRET", None))

db = SQLAlchemy(app)
oauth = OAuth(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

from app import views 