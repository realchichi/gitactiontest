import base64
import json
import http.client
# from urllib.request import urlopen
from app.forms import forms


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

@app.route('/process', methods=['POST']) 
def process(): 
    data = request.form.get('data')
    return 
@app.route('/forms/', methods=('GET', 'POST'))
def form():
    form = forms.registerForm()
    nub=0

    if form.validate_on_submit():
        raw_json = read_file('app/data/users.json')
        user = json.loads(raw_json)

        for i in user:
            if i["username"] == form.username.data.lower():
                nub+=1
                flash('Username already exists')
                break
        for i in user:
            if i["email"] == form.email.data.lower():
                nub+=1
                flash('Email already exists')
                break
        
        if nub==0:   
           bytess = form.password.data.encode('utf-8') 
           salt = bcrypt.gensalt() 
           hashy = bcrypt.hashpw(bytess, salt)
           x = hashy.decode('utf-8')
           user.append({'username': form.username.data.lower(),
                               'email': form.email.data.lower(),
                               'password': x,
                               })
           write_file('app/data/users.json',
                      json.dumps(user, indent=4))
           return redirect(url_for('login.html'))
       
    return render_template('login.html', form=form)
@app.route('/')
def home():
    return app.send_static_file('login.html')




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
