from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.db_connection import get_db
from db.person_db import PersonDB

router = APIRouter()

@router.get("/persons")
async def get_persons(db: Session = Depends(get_db)):
    persons = db.query(PersonDB).all()
    print(persons)
    return persons


@router.get("/person/{id}")
async def get_person(id: int, db: Session = Depends(get_db)):
    person = db.query(PersonDB).get(id)
    if person == None:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


@router.delete("/person/{id}")
async def delete_person(id: int, db: Session = Depends(get_db)):
    db.query(PersonDB).filter(PersonDB.id==id).delete()
    db.commit()
    return {"message": "Person deleted succesfully."}