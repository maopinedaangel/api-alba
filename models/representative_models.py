from models.address_models import Phone
from pydantic import BaseModel
from datetime import date
from typing import Optional
from models.address_models import Address, Phone

class Representative(BaseModel):
    dni: str
    firstName: str
    lastName: str
    mail: Optional[str]
    birthday: date
    occupation: str
    relationship: str
    phone: Phone
    address: Address


class RepresentativeIn(BaseModel):
    patientId: int
    representative: Representative