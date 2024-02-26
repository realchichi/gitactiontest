import base64
import json
import http.client
import requests
import os
from io import BytesIO
# from PIL import Image
from app.forms import forms
from flask import (jsonify, render_template,request, url_for, flash, redirect)
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, login_required, logout_user,current_user
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     RadioField,EmailField,PasswordField)
from wtforms.validators import InputRequired, Length,Email,Regexp,EqualTo
# from form.forms import RegistrationForm
# from urllib.request import urlopen
from app.forms.forms import RegistrationForm
# from flask_wtf import FlaskForm
from flask import (jsonify, render_template,request, url_for, flash, redirect,Flask)
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, login_required, logout_user,current_user, LoginManager
import random
import psycopg2
from app import app
from app import db
from app.models.accounts import Account
from app.models.history import History
from app.models.plantinfo import PlantInfo
# from sqlalchemy.sql import text
from app import login_manager

@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))


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
    return render_template("uploadImage.html")


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
    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')
        user = Account.query.filter_by(email=email).first()

        remember = bool(request.form.get('is_active'))
        print(user.id,"lllllllllllllllllllllllllllll")

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('landing'))

    return render_template('login.html')


@app.route("/faqs")
def feqs():
    return render_template("faqs.html")


# Written by Wachirapong
# To call validate form and store to database
@app.route("/contact_us", methods=["GET", "POST"])
def contact_us():
    if request.method == "POST":
        result = request.form.to_dict()
        # print(result)
        valid_keys = ["name", "email", "message"]
        validated_dict = {}
        validated = True

        for key in result:
            if key not in valid_keys:
                continue

            if not result[key] or result[key] == "undefined":
                validated = False
                break

            validated_dict[key] = result[key].strip()
        # if validated:
        #     contact = Contact(**validated_dict)
        #     db.session.add(contact)

        # db.session.commit()
    return render_template("contact_us.html")


# Written by Wachirapong
# To call API
@app.route("/api")
def call_api(img):
    # with open('app/static/img/longan1.jpg', 'rb') as file:
    #     images = [base64.b64encode(file.read()).decode('ascii')]

    # url = "https://plant.id/api/v3/identification"
    # DETAILS = "common_names,url,description,taxonomy,rank,gbif_id,inaturalist_id,image,synonyms,edible_parts,watering,propagation_methods"
    # query = "?details=" + DETAILS +"&language=th"
    # url += query

    # payload = json.dumps({
    #     "images": ["data:image/jpg;base64," + images[0]],
    #     "similar_images": True
    # })
    # headers = {
    #     'Api-Key': 'XbcsHOYrpQJBei7BNsrP7TeXUyerkYd1SpqRVAfSgq2T9lIZbu',
    #     'Content-Type': 'application/json'
    # }
    # if u need to call API use these 2 lines
    # response = requests.request("POST", url, headers=headers, data=payload)
    # list_data = get_data(json.loads(response.text))
    # these 2 lines for temp data
    raw_data = read_file("app/sandbox/data.txt")
    list_data = eval(raw_data)
    # return render_template("plant_data.html", data=list_data)
    return list_data


# Written by Wachirapong
# To get data from API that we need to put into list
def get_data(data):
    name = data["result"]["classification"]["suggestions"]
    list_data = []
    count = 0
    for val in name:
        dict_val = {}
        if count == 5:
            break
        dict_val["name"] = val.get("name", "N/A")
        dict_val["url_image"] = val["details"]["image"].get("value", "N/A")
        # print(val["details"]["description"])
        if val["details"]["description"]:
            dict_val["description"] = val["details"]["description"]["value"]
        else:
            dict_val["description"] = "N/A"
        dict_val["wiki_url"] = val["details"].get("url", "N/A")
        dict_val["taxonomy"] = val["details"].get("taxonomy", "N/A")
        dict_val["common_name"] = val["details"].get("common_names", "N/A")
        dict_val["similar_images"] = []
        count_img = 0
        for simi_img in val["similar_images"]:
            if count_img == 3:
                break
            dict_val["similar_images"].append(simi_img["url"])
            count_img += 1
        dict_val["probability"] = val.get("probability", "N/A")
        count += 1
        list_data.append(dict_val)
    return list_data


# Written by Wachirapong
# To store plant data table that user who identified plant
# and store it to history table
@app.route("/identification", methods=["POST", "GET"])
def identification():
    if request.method == "POST":
        result = {}
        print(request.files.keys())
        image_file = request.files['image']
        filename = os.path.join(app.config['UPLOAD_FOLDER'], 'captured_image.jpg')
        image_file.save(filename)
        # print(len(result["photoDataUrl"]))
        print(result)
        account_id = current_user.id
        if result.get("idendtfied_img",""):
            idendtfied_img = result["idendtfied_img"]
            entry = History(account_id, idendtfied_img)
            db.session.add(entry)
            history = History.query.filter_by(idendtfied_img=idendtfied_img).first()
            plant_data = call_api(idendtfied_img)
            for i in range(len(plant_data)):
                temp = plant_data[i]
                temp["history_id"] = history.id
                plant_info = PlantInfo(**temp)
                db.session.add(plant_info)

            db.session.commit()
            return render_template("plant_data.html", plant_data=plant_data)
    return render_template("identification.html")


def validate_email_domain(form, field):
    email = field.data
    allowed_domains = ['gmail.com', 'hotmail.com','cmu.ac.th']
    domain = email.split('@')[-1]
    if domain not in allowed_domains:
        raise ValidationError(f'Invalid email domain. Allowed domains are: {", ".join(allowed_domains)}')


@app.route("/signup", methods=('GET', 'POST'))
def signup():
    if request.method == 'POST' :
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
            validated_value = RegistrationForm()
            
        if   len(validated_dict["name"]) < 2 or len(validated_dict["name"])>20:
            flash('name must be between 2 and 20 characters long')
            return redirect(url_for('signup'))
        elif   not is_valid_email_domain(validated_dict["email"]) :
            flash('Email is required mush be *@gmail.com or *@hotmail.com or *@cmu.ac.th')
            return redirect(url_for('signup'))
        elif  not is_valid_password(validated_dict["password"]):
            flash('Password must contain at least 8 characters including at least one digit, one lowercase letter, one uppercase letter, and one special character')
            return redirect(url_for('signup'))
        elif validated:
            email = validated_dict['email']
            name = validated_dict['name']
            password = validated_dict['password']
            user = Account.query.filter_by(email=email).first()
            if user:
                flash('Email address already exists')
                return redirect(url_for('signup'))  
            new_user = Account(email=email, name=name, password=generate_password_hash(password, method='sha256'),avatar_url="static/img/avatar/"+str(random.randint(1, 8))+".png")
            db.session.add(new_user)

            db.session.commit()

        return redirect(url_for('login')) 
        
    return render_template("signup.html")


@app.route("/signup/data")
def si():
    db_accounts = Account.query.all()
    accounts = list(map(lambda x: x.to_dict(), db_accounts))
    return jsonify(accounts)

@app.route("/update",methods=('POST','GET'))
def update():
    if request.method == 'POST':
        result = request.form.to_dict()
        email = result.get('email','')
        name = result.get('name','')
        avatar = result.get('avatar_url','')
        password = result.get('password','')
        accounts = Account.query.get(current_user.id)
        if password == '':
            password = current_user.password
        if   len(name) < 2 or len(name)>20:
            flash('name must be between 2 and 20 characters long')
            return redirect(url_for('profile'))
        elif   not is_valid_email_domain(email) :
            flash('Email is required mush be *@gmail.com or *@hotmail.com or *@cmu.ac.th')
            return redirect(url_for('profile'))
        elif  not is_valid_password(password):
            flash('Password must contain at least 8 characters including at least one digit, one lowercase letter, one uppercase letter, and one special character')
            return redirect(url_for('profile'))
        accounts.update(email=email,name=name, avatar_url=avatar,password=generate_password_hash(password, method='sha256'))
        db.session.commit()
    return redirect(url_for('profile'))







@app.route("/checkpassword",methods=('GET','POST'))
def hw10_update():
    ans={"ans":False}
    if request.method == "POST":
        result = request.form.to_dict()
        password = result.get('password','')
        contact = Account.query.get(current_user.id)
        if check_password_hash(contact.password,password):
            ans["ans"]=True
            return ans
        else :
            flash('password not correct')
    return ans

# @app.route('/validate_email', methods=['POST'])
# def validate_email():
#     ans={"ans":False}
#     form = RegistrationForm(request.form.to_dict().get('email',''))
#     if form.validate():
#         ans["ans":True]
#         return ans

#     return ans
def is_valid_email_domain(email):
    domain = email.split('@')[-1]
    return domain in ['gmail.com', 'hotmail.com', 'cmu.ac.th']

def is_valid_password(password):
    return len(password) >= 8 and any(c.isdigit() for c in password) and any(c.islower() for c in password) and any(c.isupper() for c in password) and any(c in '!@#$%^&*()-_=+[]{}|;:,.<>?/~' for c in password)

@app.route("/history/data")
# @login_required
def history_data():
    # history = History.query.get(current_user.id)
    # plant = PlantInfo.query.get(account_id)
    history = History.query.filter(History.account_id == current_user.id)
    history_data = list(map(lambda x: x.to_dict(), history))
    return jsonify(history_data)

@app.route("/history")
# @login_required
def history():
    return render_template("history.html")

@app.route("/delete/history",methods=('GET','POST'))
@login_required
def delete_history():
    if request.method == "POST":
        result = request.form.to_dict()
        id_ = result.get('id', '')
        account_id = result.get('account_id', '')
        history = History.query.get(id_)
        if history.account_id == current_user.id:
            history = history.remove_history(account_id)
            db.session.commit()
    return history_data()