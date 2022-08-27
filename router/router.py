from email import message
from lib2to3.pytree import _Results
from typing import List
from urllib import response
from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from schema.user_schema import userSchema, dataUser
from config.db import engine
from models.users import users
from werkzeug.security import generate_password_hash, check_password_hash


router = APIRouter()


@router.get("/")
def root():
    return {"message": "Hi i'am FastAPI"}


@router.get("/api/user", response_model=List[userSchema])
def get_users():
    with engine.connect as conn:
        result = conn.execute(users.select()).fetchall()

        return result


@router.get("/api/user/{user_id}", response_model=userSchema)
def get_user(user_id: str):
    with engine.connect as conn:
        result = conn.execute(users.select().where(
            users.c.id == user_id)).first()

        return result


@router.post("/api/user", status_code=HTTP_201_CREATED)
def create_user(data_user: userSchema):
    with engine.connect() as conn:
        new_user = data_user.dict()
        new_user['user_password'] = generate_password_hash(
            data_user.user_password, "pbkdf2:sha256:30", 30)

        conn.execute(users.insert().values(new_user))

        return Response(status_code=HTTP_201_CREATED)
    
@router.post("/api/user/login", status_code=200)
def user_login(data_user: dataUser):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.username == data_user.username)).first()
        
        if result != None:
            check_pass = check_password_hash(data_user.user_password, result[3])
            
        if check_pass:
            return {"status": 200,"message": "Succes"}
        
        return  {"status": HTTP_401_UNAUTHORIZED, "message": "Access denied"}
        
@router.put("/api/user/{user_id}}", response_model=userSchema)
def update_user(data_update: userSchema, user_id: str):
    with engine.connect as conn:
        encrypt_password = generate_password_hash(
            data_update.user_password, "pbkdf2:sha256:30", 30)
        conn.execute(users.update().values(name=data_update.name,
                     username=data_update.username, user_password=encrypt_password))

        result = conn.execute(users.select().where(
            users.c.id == user_id)).first()

        return result
    
@router.delete("/api/user/{user_id}", status_code=HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
  with engine.connect() as conn:
    conn.execute(users.delete().where(users.c.id == user_id))

    return Response(status_code=HTTP_204_NO_CONTENT)
