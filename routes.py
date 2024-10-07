from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
import jwt
from models import(
    UserRegister,
    UserLogin,
)
from database import (
    find_user_by_email, 
    insert_user
)
import os

router = APIRouter()

SECRET_KEY = os.getenv('SECRET_KEY')

@router.post('/user/register')
async def user_register(user: UserRegister):
   
    already_registered_user = find_user_by_email(user.email)  # Check if user is already registered
    if already_registered_user:
        raise HTTPException(
            status_code=404, detail='User with this email already exists'
        )
    
   
    required_fields = {
        'name': user.name,
        'email': user.email,
        'password': user.password,
        'confirm_password': user.confirm_password,
    }
    missing_fields = [field for field, value in required_fields.items() if not value]  # Check for missing fields
    if missing_fields:
        raise HTTPException(
            status_code=400,
            detail=f"The following fields are mandatory: {', '.join(missing_fields)}"
        )
    
    if user.password != user.confirm_password: #check for password and confirm password must be match
        raise HTTPException(
            status_code=400, detail='Password and confirm password did not match'
        )
    
    user_inserted = insert_user(dict(user)) #insert the user into the data base
    return {
        'message': 'User registered successfully'
    }

@router.post('/user/login')
async def user_login(login: UserLogin):
    user = find_user_by_email(login.email)
    
    if not user:
        raise HTTPException(
            status_code=204, detail='User with this email does not exist'
        )
    
    data = jsonable_encoder(login.email, login.password)
   
    encoded_jwt = jwt.encode({'data': data}, SECRET_KEY, algorithm='HS256') #create the encoded token if user is login that is already registered
    
    return {
        'message': 'Login successful',
        'token': encoded_jwt
    }






