from fastapi import Depends, HTTPException, status

from typing import Union
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from sqlalchemy.orm import Session
import random

from config.config import settings
from db.db_connection import get_db
from db.user_db import UserDB, UserData, CodeDB
from models.user_models import TokenData, UserOut



SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    #print(pwd_context.hash(password))
    return pwd_context.hash(password)

def get_user(db: Session, username: str):
    user = db.query(UserDB).filter(UserDB.username == username).one()
    return user

#Función agregada para obtener datos extendidos del usuario
def get_user_data(db: Session, username: str):
    user = db.query(UserData).filter(UserData.username == username).one()
    return user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    #print(encoded_jwt)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_data(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserOut = Depends(get_current_user)):    
    #print(current_user)   
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_mail_by_username(db: Session, username: str):
    user = db.query(UserData).filter(UserData.username == username).one()
    return user.mail

#¿Repetida?
def get_user_by_username(db: Session, username: str):
    user = db.query(UserDB).filter(UserDB.username == username).one()
    return user


def generate_temporal_code():
    code = random.randint(0,999999)
    str_code = '{:06d}'.format(code)
    #print(str_code)
    return str_code


def get_user_by_code(db: Session, key: str):
    key_in_db = db.query(CodeDB).filter(CodeDB.code == key).one()
    if not key_in_db:
        return None
    user = None
    user_id = key_in_db.user_id
    #Revisar
    user = db.query(CodeDB).get(user_id)
    return user


def verify_temporal_code(db: Session, key: str, username: str):
    key_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="El pin no es válido o ha expirado"
    )
    #Falla si el código no existe. Refactorizar con try-except
    key_in_db = db.query(CodeDB).filter(CodeDB.code == key).one()
    if not key_in_db:
        raise key_exception          
    user_id = key_in_db.user_id
    user = db.query(UserDB).get(user_id).username
    if not user == username:
        raise key_exception                 
    expiration_time = key_in_db.creation_time + timedelta(minutes=15)
    current_time = datetime.utcnow()   
    if current_time > expiration_time:
        raise key_exception        
    return user_id


def update_password(db: Session, key: str, username: str, password: str):
    if verify_temporal_code != None:
        user = get_user_by_username(db, username)
        user.password = get_password_hash(password)
        db.commit()
        db.refresh(user)
        return {"message": "Contraseña actualizada exitosamente."}        
    else:
        return {"message": "Error. La contraseña no fue actualizada."} 