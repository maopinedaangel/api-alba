from pydantic import BaseModel
from typing import Optional


class UserIn(BaseModel):
    dni: str
    firstName: str
    lastName: str
    mail: Optional[str]
    role: str
    username: str
    password: str


class UserOut(BaseModel):
    userId: int
    personId: int
    dni: str
    firstName: str
    lastName: str
    role: str    
    mail: Optional[str]      
    username: str

    class Config:
        orm_mode=True    



'''
class UserOut(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
'''



'''
class UserInDB(UserOut):
    hashed_password: str
'''



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

    