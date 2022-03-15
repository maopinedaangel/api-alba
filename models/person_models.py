from pydantic import BaseModel
from typing import Optional

class NewPerson(BaseModel):
    dni: str
    firstName: str
    lastName: str
    mail: Optional[str]