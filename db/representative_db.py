from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from db.db_connection import Base, engine


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