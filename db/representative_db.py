from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from db.db_connection import Base, engine, get_db


class RepresentativeDB(Base):
    __tablename__ = "representative"

    id = Column(Integer, primary_key=True, autoincrement=True)
    personId = Column(Integer, ForeignKey('person.id'))
    patientId = Column(Integer, ForeignKey('patient.id'))
    birthday = Column(DateTime)
    occupation = Column(String)
    relationship = Column(String)


class RepresentativeData(Base):
    __tablename__ = "representative_data"

    personId = Column(Integer, primary_key=True)
    patientId = Column(Integer)
    dni = Column(String)
    firstName = Column(String)
    lastName = Column(String)
    birthday = Column(DateTime)
    relationship = Column(String)     
    occupation = Column(String)      
    address = Column(String)
    phones = Column(ARRAY(String))
    mail = Column(String)

    class Config:
        orm_mode = True

        
Base.metadata.create_all(bind=engine)


#def create_representative(representative: RepresentativeDB, db: Session = Depends(get_db)):
def create_representative(representative: RepresentativeDB, db: Session):
    db.add(representative)
    db.commit()
    db.refresh(representative) 