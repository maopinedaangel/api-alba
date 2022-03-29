from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.db_connection import get_db
from db.user_db import UserDB
from models.user_models import UserIn
from db.person_db import PersonDB
import db.user_db


router = APIRouter()


@router.get("/users")
async def get_users(database: Session = Depends(get_db)):
    return db.user_db.get_all_users(database)


@router.get("/user")
async def get_user(id: int, database: Session = Depends(get_db)):
    return db.user_db.find_user_by_id(id, database)


@router.post("/user")
async def new_user(user: UserIn, database: Session = Depends(get_db)):

    #Crea una persona que corresponde al usuario    
    person_in = {
        "dni": user.dni,
        "firstName": user.firstName,
        "lastName": user.lastName,
        "mail": user.mail
    }

    new_person = PersonDB(**person_in)
    person_id = db.person_db.create_person(new_person, database)

    user_in = {
        "personId": person_id,
        "role": user.role,
        "username": user.username,
        "password": user.password
    }

    new_user = UserDB(**user_in)    
    db.user_db.create_user(new_user, database)
    return "User created successfully"