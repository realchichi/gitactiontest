import base64
import json
import http.client
# from urllib.request import urlopen
from app.forms import forms
# from flask_wtf import FlaskForm

import psycopg2
from flask import (jsonify, render_template,request)
from app import app
# from app import db
# from sqlalchemy.sql import text
# from app.models.user import User

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
    
       
    return render_template('login.html', form=form)
# @app.route('/')
# def home():
#     # if request.method == 'POST':
#     #     result = request.form.to_dict()
#     #     validated = True
#     #     validated_dict = dict()
#     #     id_ = result.get('id', '')
#     #     valid_keys = ['email', 'password']


#     #     # validate the input
#     #     for key in result:
#     #         # screen of unrelated inputs
#     #         value = result[key].strip()
#     #         if not value or value == 'undefined':
#     #             validated = False
#     #             break
#     #         validated_dict[key] = value


#     #     if validated:
#     #         # if there is no id: create a new contact entry

#     #         if not id_:
#     #             entry = Contact(**validated_dict)
#     #             db.session.add(entry)
#     #         # if there is an id already: update the contact entry
#     #         else:
#     #             contact = Contact.query.get(id_)
#     #             contact.update(**validated_dict)


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


@app.route("/home")
def home():
    return app.send_static_file("login.html")


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


def get_data(res):
    is_plant = res["result"]["is_plant"]["probability"]
    name = res["result"]["classification"]["suggestions"]
    dict_val = {}
  # name                : latin name
  # probability         : prob that is plant
  # similar_img         : similar image
  # common_name         : common name
  # taxonomy            : taxonomy
  # url                 : wiki pedia url
  # description         : description
  # synonyms            : synonyms
  # img                 : image of this plant
  # watering            : watering how wet environment the plant prefers(1 = dry, 2 = medium, 3 = wet)
  # propagation_methods : propagation method
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



