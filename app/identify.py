import base64
import json
import requests
import http.client
from urllib.request import urlopen

def call_api():
  with open('static/img/photo1.jpg', 'rb') as file:
      images = [base64.b64encode(file.read()).decode('ascii')]

  type_iden = ["health_assessment","identification"]

  url_iden = "https://plant.id/api/v3/" + type_iden[1]
  DETAILS = "common_names,url,description,taxonomy,rank,gbif_id,inaturalist_id,image,synonyms,edible_parts,watering,propagation_methods"
  q_iden = "?details=" + DETAILS +"&language=en"
  url_iden += q_iden

  payload = json.dumps({
    "images": ["data:image/jpg;base64," + images[0]],
    "similar_images": True
  })
  headers = {
    'Api-Key': 'XbcsHOYrpQJBei7BNsrP7TeXUyerkYd1SpqRVAfSgq2T9lIZbu',
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url_iden, headers=headers, data=payload)

  return response

def get_data(res):
  is_plant = res["is_plant"]["probablity"]