from fastapi import APIRouter, Depends, HTTPException
from db.db_connection import get_db
from sqlalchemy.orm import Session

from db.address_db import AddressDB

router = APIRouter()

@router.get("/addresses")
async def get_addresses(db: Session = Depends(get_db)):
    addresses = db.query(AddressDB).all()
    return addresses


@router.get("/address/{id}")
async def get_address(id: int, db: Session = Depends(get_db)):
    address = db.query(AddressDB).get(id)
    if address == None:
        raise HTTPException(status_code=404, detail="Address not found")
    return address


@router.get("/adresses-by-person/{personId}")
async def get_addresses_by_person(personId: int, db: Session = Depends(get_db)):
    address = db.query(AddressDB).filter(AddressDB.personId == personId).one()
    return address

'''
@router.get("/phones-by-person/{personId}")
async def get_phones_by_person(personId: int, db: Session = Depends(get_db)):
    phones = db.query(PhoneDB).filter(PhoneDB.personId == personId)
    return phones
'''
