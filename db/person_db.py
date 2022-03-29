from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException


from db.db_connection import Base, engine, get_db

class PersonDB(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dni = Column(String)
    firstName = Column(String)
    lastName = Column(String)
    #revisar
    mail = Column(String, nullable=True)


Base.metadata.create_all(bind=engine)


#def create_person(person: PersonDB, db: Session = Depends(get_db)):
def create_person(person: PersonDB, db: Session):    
    db.add(person)
    db.commit()
    db.refresh(person)
    return person.id