import base64
import json
import requests
import http.client
from urllib.request import urlopen



TEMP = {
    "access_token": "NQ9ErOcn2A3QTsH",
    "model_version": "plant_id:3.4.1",
    "custom_id": "null",
    "input": {
        "latitude": "null",
        "longitude": "null",
        "similar_images": "true",
        "images": ["https://plant.id/media/imgs/08b9062e640a4200aabf16f1f29f6ee3.jpg"],
        "datetime": "2024-01-29T18:22:49.127406+00:00",
    },
    "result": {
        "is_plant": {"probability": 0.99992275, "binary": "true", "threshold": 0.5},
        "classification": {
            "suggestions": [
                {
                    "id": "f12b23ca000d0506",
                    "name": "Epipremnum aureum",
                    "probability": 0.99,
                    "similar_images": [
                        {
                            "id": "ae74da534b854b5bb274c8f48a50e4d2702332ce",
                            "url": "https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/ae7/4da534b854b5bb274c8f48a50e4d2702332ce.jpeg",
                            "similarity": 0.83,
                            "url_small": "https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/ae7/4da534b854b5bb274c8f48a50e4d2702332ce.small.jpeg",
                        },
                        {
                            "id": "13e5a7c86224ce3e4c217553e2235bdc4d362972",
                            "url": "https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/13e/5a7c86224ce3e4c217553e2235bdc4d362972.jpeg",
                            "similarity": 0.807,
                            "url_small": "https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/13e/5a7c86224ce3e4c217553e2235bdc4d362972.small.jpeg",
                        },
                    ],
                    "details": {
                        "common_names": [
                            "Golden Pothos",
                            "Ivy-arum",
                            "Silver Vine",
                            "Taro vine",
                            "Money Plant",
                            "Devil's-Ivy",
                        ],
                        "taxonomy": {
                            "class": "Liliopsida",
                            "genus": "Epipremnum",
                            "order": "Alismatales",
                            "family": "Araceae",
                            "phylum": "Tracheophyta",
                            "kingdom": "Plantae",
                        },
                        "url": "https://en.wikipedia.org/wiki/Epipremnum_aureum",
                        "gbif_id": 2868323,
                        "inaturalist_id": 69223,
                        "rank": "species",
                        "description": {
                            "value": "Epipremnum aureum is a species in the arum family Araceae, native to Mo'orea in the Society Islands of French Polynesia. The species is a popular houseplant in temperate regions but has also become naturalised in tropical and sub-tropical forests worldwide, including northern South Africa, Australia, Southeast Asia, South Asia, the Pacific Islands and the West Indies, where it has caused severe ecological damage in some cases.The plant has a number of common names including golden pothos, Ceylon creeper, hunter's robe, ivy arum, house plant, money plant, silver vine, Solomon Islands ivy, marble queen, and taro vine. It is also called devil's vine or devil's ivy because it is almost impossible to kill and it stays green even when kept in the dark. It is sometimes mistakenly labeled as a Philodendron, Pothos or Scindapsus in plant stores. It is commonly known as a money plant in many parts of the Indian subcontinent. It rarely flowers without artificial hormone supplements; the last known spontaneous flowering in cultivation was reported in 1964.The plant has gained the Royal Horticultural Society's Award of Garden Merit.",
                            "citation": "https://en.wikipedia.org/wiki/Epipremnum_aureum",
                            "license_name": "CC BY-SA 3.0",
                            "license_url": "https://creativecommons.org/licenses/by-sa/3.0/",
                        },
                        "synonyms": [
                            "Epipremnum mooreense",
                            "Pothos aureus",
                            "Rhaphidophora aurea",
                            "Scindapsus aureum",
                            "Scindapsus aureus",
                        ],
                        "image": {
                            "value": "https://plant-id.ams3.cdn.digitaloceanspaces.com/knowledge_base/wikidata/401/40124b6396a64bf855b2ee2875118b0b127489bb.jpg",
                            "citation": "//commons.wikimedia.org/wiki/User:Joydeep",
                            "license_name": "CC BY-SA 3.0",
                            "license_url": "https://creativecommons.org/licenses/by-sa/3.0/",
                        },
                        "edible_parts": "null",
                        "watering": {"max": 2, "min": 2},
                        "propagation_methods": "null",
                        "language": "en",
                        "entity_id": "f12b23ca000d0506",
                    },
                }
            ]
        },
    },
    "status": "COMPLETED",
    "sla_compliant_client": "true",
    "sla_compliant_system": "true",
    "created": 1706552569.127406,
    "completed": 1706552569.795698,
}

# def call_api():
#   with open('static/img/photo1.jpg', 'rb') as file:
#       images = [base64.b64encode(file.read()).decode('ascii')]

#   type_iden = ["health_assessment","identification"]

#   url_iden = "https://plant.id/api/v3/" + type_iden[1]
#   DETAILS = "common_names,url,description,taxonomy,rank,gbif_id,inaturalist_id,image,synonyms,edible_parts,watering,propagation_methods"
#   q_iden = "?details=" + DETAILS +"&language=en"
#   url_iden += q_iden

#   payload = json.dumps({
#     "images": ["data:image/jpg;base64," + images[0]],
#     "similar_images": "true"
#   })
#   headers = {
#     'Api-Key': 'XbcsHOYrpQJBei7BNsrP7TeXUyerkYd1SpqRVAfSgq2T9lIZbu',
#     'Content-Type': 'application/json'
#   }

#   response = requests.request("POST", url_iden, headers=headers, data=payload)

#   return response

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
  print(list_data)



get_data(TEMP)