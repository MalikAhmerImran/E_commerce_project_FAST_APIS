import jwt
import os
from dotenv import load_dotenv
from database import get_user_information

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
algorithm = os.getenv('algorithm')


def get_user(token):

    payload=jwt.decode(token,SECRET_KEY,algorithm)

    print('payload=',payload)

    

    email=payload['data']

    print('email=',email)

    user=get_user_information(email)

    return user



