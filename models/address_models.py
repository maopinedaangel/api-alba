from pydantic import BaseModel
from typing import Optional


class Address(BaseModel):
    street: str
    number: int
    crossStreetBackward: str
    crossStreetForward: str
    suburb: str
    postalCode: str
    municipality: str
    state: str

class AddressIn(BaseModel):
    personId: int
    address: Address


class Phone(BaseModel):
    number: str

class PhoneIn(BaseModel):
    personId: int
    phone: Phone