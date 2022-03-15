from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from db.db_connection import Base, engine
import datetime


class PatientDB(Base):
    __tablename__ = "patient"

    id = Column(Integer, primary_key=True, autoincrement=True)
    personId = Column(Integer, ForeignKey('person.id'))
    birthday = Column(DateTime)
    sex = Column(String)
    country = Column(String)
    civilState = Column(String)
    schoolGrade = Column(String)
    schoolLevel = Column(Integer)
    occupation = Column(String)
    salary = Column(Integer)
    healthCard = Column(String)
    isInsured = Column(Boolean)
    provider = Column(String)
    religion = Column(String)
    language = Column(String)
    bloodType = Column(String)
    rh = Column(String)



class PatientData(Base):
    __tablename__ = "patient_data"

    patientId = Column(Integer, primary_key=True)
    personId = Column(Integer)
    dni = Column(String)
    firstName = Column(String)
    lastName = Column(String)
    birthday = Column(DateTime)
    sex = Column(String)
    country = Column(String)
    civilState = Column(String)
    schoolGrade = Column(String)
    schoolLevel = Column(Integer)
    occupation = Column(String)
    salary = Column(Integer)
    healthCard = Column(String)
    isInsured = Column(Boolean)
    provider = Column(String)
    religion = Column(String)
    language = Column(String)
    bloodType = Column(String)
    rh = Column(Boolean)
    address = Column(String)
    phones = Column(ARRAY(String))
    mail = Column(String)

    class Config:
        orm_mode = True


Base.metadata.create_all(bind=engine)