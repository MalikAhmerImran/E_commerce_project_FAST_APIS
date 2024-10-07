from pymongo import MongoClient


client=MongoClient()

db = client['user']   #creating the data base with user 
user_registration = db['user_registration']




def insert_user(user_data: dict):#function that will insert the user in data base

    user_registration=user_registration.insert_one(user_data)


    return user_registration


def find_user_by_email(email: str):  #function that will return the details of registered user

    user_registration=user_registration.find_one({'email': email})

    return user_registration





