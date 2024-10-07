from pymongo import MongoClient
from fastapi import FastAPI,HTTPException
from fastapi.encoders import jsonable_encoder
import jwt
from models import  UserRegister,UserLogin
import os 
from dotenv import load_dotenv


load_dotenv()

SECRET_KEY=os.getenv('SECRET_KEY')


client=MongoClient()

user=client['user']  #creating the data base with user name
user_registration=user['user_registration']  #creating the collection with user_registration

app=FastAPI()

@app.post('/user/register')

async def user_register(user:UserRegister):

    already_registered_user=user_registration.find_one({'email':user.email}) # checking that user already registered or not

    if already_registered_user:
        raise HTTPException(
            status_code=404,detail='user with this email already exist'
        )
    required_fields = {
    'name': user.name,
    'email': user.email,
    'password': user.password,
    'confirm_password': user.confirm_password,
}

    missing_fields = [field for field, value in required_fields.items() if not value]

    if missing_fields:
        raise HTTPException(
        status_code=400,
        detail=f"The following fields are mandatory: {', '.join(missing_fields)}"
    )
   
    if user.password != user.confirm_password: # check for password and confirm password did not match
         raise HTTPException(
             status_code=400,detail='password and confirm password did not match'
         )
   
    
    user_inserted=user_registration.insert_one(dict(user)) #register the student if not already registered 


    return {
        'message':'user register successfully'
    }


@app.post('/user/login')
async def user_login(login:UserLogin):
    user=user_registration.find_one({'email':login.email})

    if not user:  # user not registered 
        raise HTTPException(
            status_code=204,detail='user with this email does not exists'
        )
    
    data=jsonable_encoder(login.email,login.password) #encoder to convert the jsonable data


    encoded_jwt=jwt.encode({'data':data},SECRET_KEY,algorithm='HS256')  #creating the token for registered user

    return {
         'message':'login successfully',
        'token':encoded_jwt
    }
    


