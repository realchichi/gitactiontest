import base64
import json
import http.client
# from urllib.request import urlopen

import psycopg2
from flask import (jsonify, render_template,request)
from app import app
from app import db
from sqlalchemy.sql import text
from app.models.user import User

READY = False

def read_file(filename, mode="rt"):
    with open(filename, mode, encoding='utf-8') as fin:
        return fin.read()

def write_file(filename, contents, mode="wt"):
    with open(filename, mode, encoding="utf-8") as fout:
        fout.write(contents)



@app.route('/db')
def db_connection():
    try:
        with db.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return '<h1>db works.</h1>'
    except Exception as e:
        return '<h1>db is broken.</h1>' + str(e)


@app.route("/home")
def home():
    return render_template("login.html")


@app.route("/camera")
def camera_access():
    return render_template("camera.html")



@app.route("/user")
def user():
    db_users = User.query.all()
    user = list(map(lambda x: x.to_dict(), db_users))
    return jsonify(user)

@app.route("/user/validate", methods=["GET", "POST"])
def validate_user():
    if request.method == "POST":
        result = request.form.to_dict()
        id_ = result.get("id", "")
        validated = True
        validated_dict = {}
        valid_keys = ["firstname", "lastname"]


@app.route("/landing")
def test():
    return render_template("landing.html")


@app.route("/login")
def test1():
    return render_template("login.html")

@app.route("/faqs")
def test2():
   return render_template("faqs.html")

@app.route("/search")
def test3():
   return render_template("search.html")

@app.route("/signup")
def test4():
    return render_template("signup.html")
