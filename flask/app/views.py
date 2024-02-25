import base64
import json
import http.client
import requests
import os
from io import BytesIO
from PIL import Image
from app.forms import forms
from flask import (jsonify, render_template,request, url_for, flash, redirect)
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, login_required, logout_user,current_user
from app import app
from app import db
from app.models.accounts import Account
from app.models.history import History
from app.models.plantinfo import PlantInfo
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
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Account.query.filter_by(email=email).first()

        remember = bool(request.form.get('is_active'))
        print(user.id,"lllllllllllllllllllllllllllll")

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('login'))
        login_user(user,remember=remember)

        return redirect(url_for('landing'))

    return render_template('login.html')


@app.route("/faqs")
def feqs():
    return render_template("faqs.html")


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
        print(request)
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

@app.route("/signup", methods=('GET', 'POST'))
def signup():
    print("1111111111111111111")
    if request.method == 'POST':
        print("2222222222222222")
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
            print("333333333333333")
            email = validated_dict['email']
            name = validated_dict['name']
            password = validated_dict['password']
            user = Account.query.filter_by(email=email).first()
            if user:
                print("4444444444")
                flash('Email address already exists')
                return redirect(url_for('signup'))  # เปลี่ยนเส้นทางไปยังหน้าลงทะเบียนอีกครั้ง
            new_user = Account(email=email, name=name, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            print("5555555555555555")
            db.session.commit()
            return redirect(url_for('login'))  # เปลี่ยนเส้นทางไปยังหน้าเข้าสู่ระบบ
        else:
            flash('Please check your input and try again.')  # เพิ่มข้อความแจ้งเตือนหากข้อมูลไม่ถูกต้อง
            return redirect({{url_for('signup')}})  # เปลี่ยนเส้นทางไปยังหน้าลงทะเบียนอีกครั้ง
    return render_template("signup.html")


@app.route("/signup/data")
def si():
    db_contacts = Account.query.all()
    contacts = list(map(lambda x: x.to_dict(), db_contacts))

    app.logger.debug(f"DB Contacts: {contacts}")

    return jsonify(contacts)


@app.route("/history")
@login_required
def history():
    return ""


