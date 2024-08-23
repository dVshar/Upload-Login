import jwt
from django.conf import settings

def decode_token(token):
    decoded_token_er = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    return decoded_token_er

def encode_token(data):
    token = jwt.encode(data, settings.SECRET_KEY, algorithm='HS256')
    return token