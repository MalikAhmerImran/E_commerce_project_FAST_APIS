from pymongo import MongoClient
from typing import Optional
from bson import ObjectId
from fastapi import HTTPException

client=MongoClient()

 #creating the data base with user 

db = client['user']  
user_registration = db['user_registration']
Products=db['Products']


#function that will insert the user in data base

def insert_user(user_data: dict):

    user=user_registration.insert_one(user_data)


    return user


#function that will return the details of registered user

def find_user_by_email(email: str):  

    user=user_registration.find_one({'email': email})

    return user


def get_user_information(email:str):

    user=user_registration.find_one({'email':email})

    return user


# function for inserting the product into the mongo db

def insert_product(product_data:dict):

    product_data=Products.insert_one(product_data)

    return product_data


#function to get the product for update

def get_product(product_id):

    product=Products.find_one({'_id':ObjectId(product_id)})


    return product

#function to update the product 

def update_product(product:dict,product_id):


    result = Products.update_one(
        {"_id": ObjectId(product_id)},  # Filter by product ID
        {"$set": product}  # Set the new data
    )
    
    return result


#function to get the product 
  
def list_products(query:Optional[dict]):

    print(query)

    if query:
        products=list(Products.find(query,{'_id':0,'token':0}))
        print(products)
    
    else:
        products=list(Products.find({},{'_id':0,'created_by':0,'token':0}))

    return products


# def list_products():

#     products=list(Products.find({},{'_id':0,'created_by':0,'token':0}))

#     return products