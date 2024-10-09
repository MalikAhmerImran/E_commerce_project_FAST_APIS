from fastapi import APIRouter, HTTPException,Request
from fastapi.encoders import jsonable_encoder
from typing import Optional
import jwt
from models import(
    UserRegister,
    UserLogin,
    Product,
    ShoppingCart,
    Cart
)
from database import (
    find_user_by_email, 
    insert_user,
    insert_product,
    get_product,
    insert_product,
    update_product,
    list_products,
    insert_cart
)

from utils import get_user
import os

router = APIRouter()

SECRET_KEY = os.getenv('SECRET_KEY')
algorithm = os.getenv('algorithm')

 # Check if user is already registered
@router.post('/user/register')
async def user_register(user: UserRegister):
   
    already_registered_user = find_user_by_email(user.email) 
    if already_registered_user:
        raise HTTPException(
            status_code=409, detail='User with this email already exists'
        )
    
   
    required_fields = {
        'name': user.name,
        'email': user.email,
        'password': user.password,
        'confirm_password': user.confirm_password,
    }

    # Check for missing fields

    missing_fields = [field for field, value in required_fields.items() if not value]  
    if missing_fields:
        raise HTTPException(
            status_code=400,
            detail=f"The following fields are mandatory: {', '.join(missing_fields)}"
        )
    
    #check for password and confirm password must be match

    if user.password != user.confirm_password: 
        raise HTTPException(
            status_code=400, detail='Password and confirm password did not match'
        )
    
    #insert the user into the data base

    user_inserted = insert_user(dict(user)) 
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

    #create the encoded token if user is login that is already registered
   
    encoded_jwt = jwt.encode({'data': data}, SECRET_KEY,algorithm) 
    
    return {
        'message': 'Login successful',
        'token': encoded_jwt
    }


#functions for CRUD operations of products

@router.post('/product/create')
async def product_create(product:Product):

    user=get_user(product.token)

    if user['is_admin'] is False:

        raise HTTPException(
            status_code=403, detail='your can not add the product because you are not the user'
        )
    
    product_data = {
        "name": product.name,
        "price": product.price,
        "category": product.category,
        "created_by": user["_id"]  # Reference to the admin who created the product
    }
    
    products=insert_product(dict(product_data))

    return {
        'message':"created successfully"
    }


# function for updating the product
@router.patch('/product/update/{product_id}')

async def  product_update(product_id:str,product:Product):

    product_found=get_product(product_id)

    if not product_found:
        
        raise HTTPException(
            status_code=204,detail='product not found'
        )
    
    product=update_product(dict(product),product_id)

    return{
        'message':'product updated successfully'
    }


# function for listing the product
@router.get('/product/list')
async def  get_products():

    products=list_products(None)
    return {
        'products':list(products)
    }


#funtion for searching the products based on categories
@router.get('/product/search')
async def searching_product(name:Optional[str]=None,category:Optional[str]=None,price:Optional[int]=None):

    query={}

    if name:
        query['name']=name

    elif category:
        query['category']=category

    elif price:
        query['price']=price

    if not query:
        raise HTTPException(
            status_code=204,detail='product not found'

        )

    products=list_products(query)

    if not products:
        raise HTTPException(
            status_code=204,detail='product not found'
        )
    
    return products

#CRUD operations for shopping cart module

#creating the shopping cart
@router.post('/cart/add/{product_id}')
async def add_product_to_cart(product_id:str,cart:Cart):

   

    user=get_user(cart.token)

    product=get_product(product_id)

    price=product['price']



    data={
        'items':product,
        'quantity':cart.quantity,
        'sub_total':cart.quantity*price,
        'customer_id':user['_id']
    }

    print(data['sub_total'])

    results=insert_cart(data)

    return {
        'massage':'Added to cart '
    }

@router.post('/cart/get')
async def get_cart_details():
    pass



    











      












