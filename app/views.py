import base64
import json
import http.client
# from urllib.request import urlopen

from flask import jsonify, render_template
from app import app, create_app
import psycopg2


def read_file(filename, mode="rt"):
    with open(filename, mode, encoding='utf-8') as fin:
        return fin.read()

def write_file(filename, contents, mode="wt"):
    with open(filename, mode, encoding="utf-8") as fout:
        fout.write(contents)

# plant_data = create_app()
conn = psycopg2.connect(
    host="test",
    database="plant_data",
    user="postgres",
    password="password"
)
cursor = conn.cursor()
table = '''CREATE TABLE plant_data (plant_id VARCHAR(45), name VARCHAR(255))'''
# cursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")
# cursor.execute('''INSERT INTO customers (name, address) VALUES ('wachi', '510')''')
# conn.commit()


# rows = cursor.fetchall()
# for row in rows:
#     print(row)


@app.route("/")
def call_api():
  # with open('static/img/photo1.jpg', 'rb') as file:
  #     images = [base64.b64encode(file.read()).decode('ascii')]

  # type_iden = ["health_assessment","identification"]

  # url_iden = "https://plant.id/api/v3/" + type_iden[1]
  # DETAILS = "common_names,url,description,taxonomy,rank,gbif_id,inaturalist_id,image,synonyms,edible_parts,watering,propagation_methods"
  # q_iden = "?details=" + DETAILS +"&language=en"
  # url_iden += q_iden

  # payload = json.dumps({
  #   "images": ["data:image/jpg;base64," + images[0]],
  #   "similar_images": "true"
  # })
  # headers = {
  #   'Api-Key': 'XbcsHOYrpQJBei7BNsrP7TeXUyerkYd1SpqRVAfSgq2T9lIZbu',
  #   'Content-Type': 'application/json'
  # }

  # response = requests.request("POST", url_iden, headers=headers, data=payload)

  # list_data = get_data(response)
  raw_data = read_file("app/sandbox/Tle_sandbox/fake_data.txt")
  fake_data = get_data(eval(raw_data))
  # print(fake_data)


  return render_template("temp.html", data=fake_data)


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



