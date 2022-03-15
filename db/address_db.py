from sqlalchemy import Column, String, Integer, ForeignKey
from db.db_connection import Base, engine


class AddressDB(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, autoincrement=True)
    personId = Column(Integer, ForeignKey('person.id'))
    street = Column(String)
    number = Column(Integer)
    crossStreetBackward = Column(String)
    crossStreetForward = Column(String)
    suburb =Column(String)
    postalCode = Column(String)
    municipality = Column(String)
    state = Column(String)


class PhoneDB(Base):
    __tablename__ = "phone"

    id = Column(Integer, primary_key=True, autoincrement=True)
    personId = Column(Integer, ForeignKey('person.id'))
    number = Column(String)

Base.metadata.create_all(bind=engine)