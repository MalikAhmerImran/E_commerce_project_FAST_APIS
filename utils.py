import jwt
import os
from database import get_user_information



SECRET_KEY = os.getenv('SECRET_KEY')
algorithm = os.getenv('algorithm')


def get_user(token):

    payload=jwt.decode(token,SECRET_KEY,algorithm)

    email=payload['data']

    user=get_user_information(email)

    return user



