import base64
import json
import requests
import http.client
from urllib.request import urlopen


with open('heal.jpg', 'rb') as file:
    images = [base64.b64encode(file.read()).decode('ascii')]

type_iden = ["health_assessment","identification"]

url_iden = "https://plant.id/api/v3/" + type_iden[1]
url_heal = "https://plant.id/api/v3/" + type_iden[0]
DETAILS = "common_names,url,description,taxonomy,rank,gbif_id,inaturalist_id,image,synonyms,edible_parts,watering,propagation_methods"
q_iden = "?details=" + DETAILS +"&language=en"
q_heal = "?full_disease_list=true&details=local_name,description,url,treatment,classification,common_names,cause"
url_iden += q_iden
url_heal += q_heal



payload = json.dumps({
  "images": ["data:image/jpg;base64," + images[0]],
  "similar_images": True
})
headers = {
  'Api-Key': 'XbcsHOYrpQJBei7BNsrP7TeXUyerkYd1SpqRVAfSgq2T9lIZbu',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url_heal, headers=headers, data=payload)

print(response.text)