import jwt
from django.conf import settings

import pymongo
client = pymongo.MongoClient("mongodb+srv://dvsharma064:admin@webjini.tom4l8g.mongodb.net/")
db = "Swaraj_Udyog"


def decode_token(token):
    decoded_token_er = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    return decoded_token_er

def encode_token(data):
    token = jwt.encode(data, settings.SECRET_KEY, algorithm='HS256')
    return token


import uuid
def add_authority_letter():
    data = {
            "createdDate":"",
            "Location":"",
            "no_od_orders":"",
            "orders":[{"sno":"","date":"","qty":""}],
            "Representative":"",
            "aadhar":"",
            "pan":"",
            "vehicle_no":""
        }
    
