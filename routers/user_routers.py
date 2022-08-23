from fastapi import APIRouter, Depends, HTTPException, status, Form
from typing import List
from datetime import timedelta

from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm

from db.db_connection import get_db
from db.user_db import UserDB, CodeDB
from models.user_models import UserIn, UserOut, Token
from db.person_db import PersonDB
import db.user_db
from service.user_service import get_password_hash, authenticate_user, create_access_token, get_current_active_user
from service.user_service import get_user_by_username, get_user_data, generate_temporal_code, get_user_by_code, verify_temporal_code, update_password, get_mail_by_username
from service.util import send_mail


ACCESS_TOKEN_EXPIRE_MINUTES = 30
router = APIRouter()




@router.get("/users", response_model=List[UserOut])
async def get_users(database: Session = Depends(get_db)):
    return db.user_db.get_all_users(database)



'''
@router.get("/user")
async def get_user(id: int, database: Session = Depends(get_db)):
    return db.user_db.find_user_by_id(id, database)
'''


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):       
    user = authenticate_user(db, form_data.username, form_data.password)    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Métodos de prueba para verificar el funcionamiento del sistema de seguridad

@router.get("/users/me", response_model=UserOut)
#Modificar:
#async def read_users_me(current_user: UserOut = Depends(get_current_active_user)):
#Modificado:
async def read_users_me(current_user: UserDB = Depends(get_current_active_user)):
    return current_user

@router.get("/users/me/items")
#Modificar:
#async def read_own_items(current_user: UserOut = Depends(get_current_active_user)):
#Modificado:
#async def read_own_items(current_user: UserDB = Depends(get_current_active_user)):
#otra vez modificado
async def read_own_items(current_user: UserDB = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]



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
        "password": get_password_hash(user.password)
    }

    new_user = UserDB(**user_in)    
    db.user_db.create_user(new_user, database)
    return "User created successfully"


'''
@router.put("/password")
async def change_password(new_password: str, current_user: UserDB = Depends(get_current_active_user),  db: Session = Depends(get_db)):
    current_user.password = get_password_hash(new_password)
    db.commit()
    db.refresh(current_user)


@router.put("/forcepassword")
async def force_password_change(new_password: str, user: str, db: Session = Depends(get_db)):
    current_user = db.query(UserDB).filter(user == UserDB.username).one()
    current_user.password = get_password_hash(new_password)
    db.commit()
    db.refresh(current_user)
'''


#@router.get("/mail/{username}")
@router.get("/mail")
async def find_mail_by_username(username: str, db: Session = Depends(get_db)):
    return { "mail": get_mail_by_username(db, username)}


# Revisar. Este método envía información privada. Enviar solo el mail.
@router.get("/user-by-username/{username}")
async def find_user_by_username(username: str, db: Session = Depends(get_db)):
    return get_user_by_username(db, username)

@router.get("/code")
async def generate_key(username: str, db: Session = Depends(get_db)):
    user = get_user_by_username(db, username)
    if user is None:
        return { "message": "El usuario no existe en la base de datos."}
    code = generate_temporal_code()
    key_data = {
        "user_id": user.id,
        "code": code
    }
    key = CodeDB(**key_data)
    db.add(key)    
    db.commit()
    db.refresh(key)
    user_data = get_user_data(db, username)
    addressee = user_data.mail
    text = "Para restablecer su contraseña, escriba el código " + code + " y su nueva contraseña en los campos indicados en el portal de Auriga. Este código solo podrá ser usado una vez, y expirará en 15 minutos."
    subject = "Restablecer contraseña Auriga"
    send_mail(addressee, subject, text)
    return { "code": code }


@router.post("/code")
async def verify_key(key: str = Form(...), username: str = Form(...), new_password: str = Form(...), db: Session = Depends(get_db)):
    return { "verified": verify_temporal_code(db, key, username), "code": key }


@router.post("/reset-password")
async def reset_password(key: str = Form(...), username: str = Form(...), new_password: str = Form(...), db: Session = Depends(get_db)):
    return update_password(db, key, username, new_password) 