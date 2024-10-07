from pymongo import MongoClient
from models import User
from fastapi import FastAPI,HTTPException


client=MongoClient()

user=client['user']  #creating the data base with user name
user_registration=user['user_registration']  #creating the collection with user_registration

app=FastAPI()

@app.post('/register/')

async def user_registraion(user:User):

    already_registered_user=user_registration.find_one({'email':user.email}) # checking that user already registered or not

    if already_registered_user:
        raise HTTPException(
            status_code=404,detail='user with this email already exist'
        )
    if not user.name :
        raise HTTPException(
            status_code=404,detail='name field is required'
        ) 
    
    if not user.email :
        raise HTTPException(
            status_code=404,detail='email field is required'
        ) 
    if not user.password :
        raise HTTPException(
            status_code=404,detail='password field is required'
        ) 
    if not user.confirm_password:
        raise HTTPException(
            status_code=404,detail='confirm password  field is required'
        ) 
        
    if user.password != user.confirm_password:
         raise HTTPException(
             status_code=404,detail='password and confirm password did not match'
         )
   
    
    user_inserted=user_registration.insert_one(dict(user)) #register the student if not already registered 

    print(type(user))


    return {
        'message':'user register successfully'
    }


