import base64
import json
import http.client
# from urllib.request import urlopen
from app.forms import forms
# from flask_wtf import FlaskForm
from flask import (jsonify, render_template,request, url_for, flash, redirect)
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, login_required, logout_user,current_user, LoginManager
import random
import psycopg2
from app import app

from app import db
# from sqlalchemy.sql import text
from app.models.accounts import Account
from app import login_manager

@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))

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

# @app.route('/')
# def home():
#     return app.send_static_file('login.html')


#     #         db.session.commit()
#     return app.send_static_file('login.html')


@app.route('/db')
def db_connection():
    try:
        with db.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return '<h1>db works.</h1>'
    except Exception as e:
        return '<h1>db is broken.</h1>' + str(e)

@app.route("/")
def home():
    return render_template("landing.html")

@app.route("/landing")
def landing():
    return render_template("landing.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/camera")
def camera_access():
    return render_template("camera.html")


# @app.route("/api")
# def call_api():
#     if READY:
#       with open('static/img/photo1.jpg', 'rb') as file:
#           images = [base64.b64encode(file.read()).decode('ascii')]

#       type_iden = ["health_assessment","identification"]

#       url_iden = "https://plant.id/api/v3/" + type_iden[1]
#       DETAILS = "common_names,url,description,taxonomy,rank,gbif_id,inaturalist_id,image,synonyms,edible_parts,watering,propagation_methods"
#       q_iden = "?details=" + DETAILS +"&language=en"
#       url_iden += q_iden

#       payload = json.dumps({
#         "images": ["data:image/jpg;base64," + images[0]],
#         "similar_images": "true"
#       })
#       headers = {
#         'Api-Key': 'XbcsHOYrpQJBei7BNsrP7TeXUyerkYd1SpqRVAfSgq2T9lIZbu',
#         'Content-Type': 'application/json'
#       }

#       response = requests.request("POST", url_iden, headers=headers, data=payload)

#   # list_data = get_data(response)

#       raw_data = read_file("app/sandbox/Tle_sandbox/fake_data.txt")
#       fake_data = list(map(lambda x : get_data(eval(x)), raw_data))
#   # list_data = 
#   # db_plant = 
#   # print(fake_data)


#   return render_template("temp.html", data=fake_data)

@app.route("/user")
def user():
    db_users = Account.query.all()
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



@app.route("/login",methods=('GET','POST'))
def login():
    logout_user()
    print(current_user.is_authenticated,"1111111111111111111111111111111")
    if request.method == 'POST':
        print(current_user.is_authenticated,"000000000000000000000000000000000")

        email = request.form.get('email')
        password = request.form.get('password')
        user = Account.query.filter_by(email=email).first()
        # remember = bool(request.form.get('is_active'))
        # print(user.id,"lllllllllllllllllllllllllllll")
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('landing'))
    print(current_user.is_authenticated,"222222222222222222222222222222")

    return render_template('login.html')

@app.route("/faqs")
def feqs():
    return render_template("faqs.html")

# Written by Wachirapong
# To call API
@app.route("/api")
def call_api():
    # if READY:
    #     with open('static/img/photo1.jpg', 'rb') as file:
    #         images = [base64.b64encode(file.read()).decode('ascii')]

    #     type_iden = ["health_assessment","identification"]

    #     url_iden = "https://plant.id/api/v3/" + type_iden[1]
    #     DETAILS = "common_names,url,description,taxonomy,rank,gbif_id,inaturalist_id,image,synonyms,edible_parts,watering,propagation_methods"
    #     q_iden = "?details=" + DETAILS +"&language=en"
    #     url_iden += q_iden

    #     payload = json.dumps({
    #         "images": ["data:image/jpg;base64," + images[0]],
    #         "similar_images": "true"
    #     })
    #     headers = {
    #         'Api-Key': 'XbcsHOYrpQJBei7BNsrP7TeXUyerkYd1SpqRVAfSgq2T9lIZbu',
    #         'Content-Type': 'application/json'
    #     }

    #     response = requests.request("POST", url_iden, headers=headers, data=payload)

  # list_data = get_data(response)

    raw_data = read_file("app/sandbox/Tle_sandbox/fake_data.txt")
    data_list = eval(raw_data)
    
    fake_data = list(map(lambda x : get_data(x), data_list))
    # list_data = 
    # db_plant = 
    # print(fake_data)


    return render_template("plant_data.html", data=fake_data)


# Written by Wachirapong
# To get data from API that we need to list
def get_data(res):
    is_plant = res["result"]["is_plant"]["probability"]
    name = res["result"]["classification"]["suggestions"]
    dict_val = {}

    list_data = []
    for val in name:
        dict_val["id"] = val["id"]
        dict_val["name"] = val["name"]
        dict_val["probability"] = val["probability"]
        dict_val["similar_img"] = val["similar_images"]
        dict_val["common_name"] = val["details"]["common_names"]
        dict_val["taxonomy"] = val["details"]["taxonomy"]
        dict_val["url"] = val["details"]["url"]
        dict_val["description"] = val["details"]["description"]["value"]
        dict_val["synonyms"] = val["details"]["synonyms"]
        dict_val["img"] = val["details"]["image"]["value"]
        dict_val["watering"] = val["details"]["watering"]
        dict_val["propagation_methods"] = val["details"]["propagation_methods"]
        list_data.append(dict_val)
    return list_data


@app.route("/search")
def search():
   return render_template("search.html")

@app.route("/signup", methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        result = request.form.to_dict()
        validated = True
        validated_dict = {}
        valid_keys = ['email', 'name', 'password']
        for key in result:
            if key not in valid_keys:
                continue
            value = result[key].strip()
            if not value or value == 'undefined':
                validated = False
                break
            validated_dict[key] = value
        if validated:
            email = validated_dict['email']
            name = validated_dict['name']
            password = validated_dict['password']
            user = Account.query.filter_by(email=email).first()
            if user:
                flash('Email address already exists')
                return redirect(url_for('signup'))  # เปลี่ยนเส้นทางไปยังหน้าลงทะเบียนอีกครั้ง
            print(current_user.is_authenticated,"4444444444444444444444444")
            new_user = Account(email=email, name=name, password=generate_password_hash(password, method='sha256'),avatar_url="static/img/avatar/"+str(random.randint(1, 7))+".png")
            print(current_user.is_authenticated,"333333333333333333333333333")
            db.session.add(new_user)
            print(current_user.is_authenticated,"555555555555555555555555555")

            db.session.commit()
            print(current_user.is_authenticated,"6666666666666666666666666")

        return redirect(url_for('login'))  # เปลี่ยนเส้นทางไปยังหน้าเข้าสู่ระบบ
        
    return render_template("signup.html")





@app.route("/signup/data")
def si():
    db_contacts = Account.query.all()
    contacts = list(map(lambda x: x.to_dict(), db_contacts))

    app.logger.debug(f"DB Contacts: {contacts}")

    return jsonify(contacts)