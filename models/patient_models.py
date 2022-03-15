from pydantic import BaseModel
from datetime import date
from typing import Optional
from models.address_models import Address, Phone
from models.representative_models import Representative


class NewPatient(BaseModel):
    dni: str
    firstName: str
    lastName: str
    mail: Optional[str]
    birthday: date
    sex: str
    country: str
    civilState: str
    schoolGrade: str
    schoolLevel: int
    occupation: str
    salary: float
    isInsured: bool
    provider: Optional[str]
    healthCard: str
    religion: str
    language: str
    bloodType: Optional[str]
    rh: Optional[bool]
    phone1: Phone
    phone2: Optional[Phone]
    address: Address
    representative: Representative



