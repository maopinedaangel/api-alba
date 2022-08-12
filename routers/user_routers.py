from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from db.db_connection import get_db
from db.user_db import UserDB, UserData
from models.user_models import UserIn, UserOut, Token, TokenData
#from models.user_models import UserInDB
from db.person_db import PersonDB
import db.user_db
from config.config import settings


SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    print(pwd_context.hash(password))
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


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(encoded_jwt)
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
        raise 
    #modificar
    #user = get_user(fake_users_db, username=token_data.username)
    #modificado (funciona):
    #user = get_user(db, username=token_data.username)
    #modificado para obtener datos extendidos del usuario:
    user = get_user_data(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

#Modificar
#async def get_current_active_user(current_user: UserOut = Depends(get_current_user)):
#Modificado:
async def get_current_active_user(current_user: UserDB = Depends(get_current_user)):    
    print(current_user)   
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


'''
@router.get("/users")
async def get_users(database: Session = Depends(get_db)):
    return db.user_db.get_all_users(database)
'''


'''
@router.get("/user")
async def get_user(id: int, database: Session = Depends(get_db)):
    return db.user_db.find_user_by_id(id, database)
'''


@router.post("/token", response_model=Token)
#Modificar:
#async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#Modificado:
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):    
    #modificar
    #user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    #modificado:
    
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
