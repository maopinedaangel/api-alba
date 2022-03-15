from sqlalchemy import Column, String, Integer
from db.db_connection import Base, engine


class PersonDB(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dni = Column(String)
    firstName = Column(String)
    lastName = Column(String)
    #revisar
    mail = Column(String, nullable=True)


Base.metadata.create_all(bind=engine)