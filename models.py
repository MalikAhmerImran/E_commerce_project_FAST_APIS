from pydantic import BaseModel


#creating the model of user 

class UserRegister(BaseModel):   
    name:str
    email:str
    password:str
    confirm_password:str
    is_admin:bool=False


#creating the model of user login

class UserLogin(BaseModel): 
    email:str
    password:str



#creating the model of product

class Product(BaseModel):
    name:str
    price:int
    description:str
    category:str
    token:str
   
    
#creating the model of shopping cart 

class ShoppingCart(BaseModel):
    customer_id:str
    items:dict
    quantity:int
    sub_total:int
    tax:int
    shipping:int
    
class Cart(BaseModel):
    quantity:int
    token:str

    