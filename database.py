from pymongo import MongoClient
from typing import Optional
from bson import ObjectId
from fastapi import HTTPException

client=MongoClient()

 #creating the data base with user 

db = client['user']  
user_registration = db['user_registration']
Products=db['Products']
Shopping_Cart=db['Shopping_Cart']


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


#functions for shopping cart

#function to add items in cart

def insert_cart(data:dict):

    results=Shopping_Cart.insert_one(data)

    return results

#function to get the cart details

def get_cart_detail(email:str):

    results = Shopping_Cart.find({'customer_id': email}, {'_id': 0, 'items._id': 0,'items.created_by':0,'items.token':0})

    result_list = list(results)

    return result_list



# function to get user purchase history
def get_user_history(email: str):

    history = Shopping_Cart.find({'customer_id': email}, {'_id': 0, 'items.name': 1})
    product_names = [item['items']['name'] for item in history]
    return product_names

# function to get similar products based on history
def get_similar_products(purchased_product_names: list):
    # Find products in the same category or with similar names
    query = {"name": {"$in": purchased_product_names}}
    similar_products = list(Products.find(query, {'_id': 0, 'created_by': 0, 'token': 0}))
    return similar_products
