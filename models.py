from pydantic import BaseModel

class UserRegister(BaseModel):   #creating the model of user 
    name:str
    email:str
    password:str
    confirm_password:str


class UserLogin(BaseModel): #creating the model of user login
    email:str
    password:str



    