from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBearer
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Optional, List
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from config.database import base, motor, session
from models.users import Users as UsersModel
from jwt_config import token_generate, token_validate
app = FastAPI()
app.title = "User registration app"

in_administrator = False

# Base from database.py
base.metadata.create_all(bind = motor)

class User_auth(BaseModel):
    email_auth: str
    pass_auth: str

class Users(BaseModel):
    id: Optional[int] = None
    userName: str
    email: str 
    password: str
    role: str 
    administrator: bool

    class config: 

        json_schema_extra = {
            "example" : {
                "username":"bogdanRivera",
                "email":"bogdanrivera@gmail.com",
                "password":"1234",
                "role":"dev",
                "administrator": True
            }
        }

class Validator(HTTPBearer):
    
    async def __call__(self, request: Request):
        global in_administrator  # Declarando in_administrator como global
        autorization = await super().__call__(request)
        db = session()
        response = db.query(UsersModel).all()
        data = token_validate(autorization.credentials)
        user = db.query(UsersModel).filter(UsersModel.email == data['email_auth']).first()
        if not user and not (data["email_auth"] == 'generic@bkgr.mx'):
            raise HTTPException(status_code=403, detail='Not authorized')
        elif data["email_auth"] == 'generic@bkgr.mx' and not response:
            in_administrator = True
        elif response and user:
            if user.administrator:
                in_administrator = True
            else:
                in_administrator = False

        
#Endpoint    
@app.get('/', response_class=HTMLResponse, tags=['EndPoint'])
def message(request: Request):
    current_path = request.base_url
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Inicio - Mi Aplicación FastAPI</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f8f9fa;
                color: #343a40;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }}
            h1 {{
                color: #007bff;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to my Fast Api app</h1>
            <p>This project is related to the registration of users</p>
            <p>Use <a href="{current_path}docs">this link</a> to try my app</p>
        </div>
    </body>
    </html>
    """
    return html_content

#Function to eliminate password for responses
def user_to_dict(user: Users):
    user_dict = user.__dict__
    user_dict.pop('password', None)  
    return user_dict

#Get all users
@app.get('/users', tags=['Users'], response_model=List[Users], status_code=200, dependencies=[Depends(Validator())])
def get_users_all() -> dict: 
    db = session()
    response = db.query(UsersModel).all()
    
    if not response:
        return JSONResponse(content={"message":"Empty database"},status_code=400)
    
    users_dict = [user_to_dict(user) for user in response]
    
    return JSONResponse(content=jsonable_encoder(users_dict),status_code=200)

#Get users by id
@app.get('/users/{id}', tags=['Users'], response_model=Users, status_code=200, dependencies=[Depends(Validator())])
def get_users_by_id(id : int) -> dict: 
    db = session()
    response = db.query(UsersModel).filter(UsersModel.id == id).first()

    if not response:
        return JSONResponse(content={"message":"Item does not exist"},status_code=400)
    
    return JSONResponse(content=jsonable_encoder(response),status_code=200)

#Get users by email
@app.get('/users/', tags = ['Users'], response_model= Users, status_code=200, dependencies = [Depends(Validator())])
def get_users_by_email(email_user : str) -> dict:
    db = session()
    response = db.query(UsersModel).filter(UsersModel.email == email_user).all()

    if not response: 
        return JSONResponse(content={"message":"Email does not exist"},status_code=400)
    
    return JSONResponse(content=jsonable_encoder(response),status_code=200)

#Add new user to DB
@app.post('/users', tags=['Users'], response_model= dict, status_code=201, dependencies=[Depends(Validator())])
def post_user(user : Users) -> dict:
    global in_administrator 
    db = session()
    response = db.query(UsersModel).all() # Obtains all registers
    
    if in_administrator and response: # If user have administrator permissions and DB is not null
        validate_user = db.query(UsersModel).filter(UsersModel.email == user.email).first() 
        if validate_user: 
            if validate_user.email == user.email:
                return JSONResponse(content={'message':'Failed to register user: User already exist in database'})
        new_user = UsersModel(**user.dict())
        db.add(new_user)
        db.commit()
        return JSONResponse(content={'message':'User registered'},status_code=200)
    elif not response: # If database is empty (First Time using the app)
        new_user = UsersModel(**user.dict())
        new_user.administrator = True
        db.add(new_user)
        db.commit()
        in_administrator = False # Once the first user is registered, permissions are changed.
        return JSONResponse(content={'message':'First time: User registered as administrator'},status_code=200)
    else:    
        return JSONResponse(content={'message':'You need administrator permissions'},status_code=200)

# Login route
@app.post('/login', tags=["Login"])
def login(user_auth : User_auth) -> dict:
    db = session()
    response = db.query(UsersModel).all()
    user = db.query(UsersModel).filter(UsersModel.email == user_auth.email_auth).first()

    if (not user or user.password != user_auth.pass_auth) and response:
        return JSONResponse(content={'message':'Invalid user or password'},status_code=401)
    elif not response: #If database is empty (First Time using the app)
        user_auth.email_auth = "generic@bkgr.mx" #Generate an generic user (This user is not added to the database.)
        user_auth.pass_auth = "1234"
    
    token : str = token_generate(user_auth.dict())

    return JSONResponse(status_code=200,content=token)

#Update user by id
@app.put('/users', tags=['Users'], response_model= dict, status_code=201, dependencies=[Depends(Validator())])
def update_user_by_id(user_id : Users, id: int) -> dict:
    mess = ""
    db = session()
    result = db.query(UsersModel).filter(UsersModel.id == id).first()

    validate_user = db.query(UsersModel).filter(UsersModel.email == user_id.email and UsersModel.id != id).first()
    if not result: 
        return JSONResponse(status_code=400, content={"message":"Update failed"})
    
    if validate_user:
        mess += "Email already exist in database, change in mail failed. "
    else: 
        result.email = user_id.email
    
    result.userName = user_id.userName
    result.password = user_id.password
    result.role = user_id.role
    if in_administrator:
        result.administrator = user_id.administrator
        mess += "You have administrator permissions, your change in 'in_administrator' was successfully"
    else:
        mess += "You don't have administrator permissions, your change in 'in_administrator' failed"

    db.commit()
    return JSONResponse(content={'mensaje':f'User updated: {mess}'},status_code=201)

#Delete user by id
@app.delete('/users/by_id', tags=['Users'], response_model=dict, status_code=200, dependencies=[Depends(Validator())])
def delete_user_by_id(id : int):
    db = session()
    result = db.query(UsersModel).filter(UsersModel.id == id).first()
    bd_have_administrator = db.query(UsersModel).filter(UsersModel.administrator == True).all()
    if not result: 
        return JSONResponse(content={'message':"Failed to delete item, item does not exist"},status_code=400)
    
    if len(bd_have_administrator)<= 1 and result.administrator:
        return JSONResponse(content={'message':'Failed to delete item, you need at least 1 administrator'},status_code=400)
    
    db.delete(result)
    db.commit()
    return JSONResponse(content={'message':'Item deleted'},status_code=200)

#Deleye user by email
@app.delete('/users/by_email', tags=['Users'], response_model=dict, status_code=200, dependencies=[Depends(Validator())])
def delete_user_by_email(user_email : str):
    db = session()
    result = db.query(UsersModel).filter(UsersModel.email == user_email).first()
    bd_have_administrator = db.query(UsersModel).filter(UsersModel.administrator == True).all()
    if not result: 
        return JSONResponse(content={'message':'Failed to delete item'},status_code=400)
    
    if len(bd_have_administrator)<= 1 and result.administrator:
        return JSONResponse(content={'message':'Failed to delete item, you need at least 1 administrator'},status_code=400)
    
    db.delete(result)
    db.commit()
    return JSONResponse(content={'message':'Item deleted'},status_code=200)
    


    
    

     




