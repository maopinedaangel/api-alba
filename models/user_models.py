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

