from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import Session
from db.db_connection import Base, engine



class UserDB(Base):
    __tablename__ = "auriga_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    personId = Column(Integer, ForeignKey('person.id'))
    role = Column(String)
    username = Column(String)
    password = Column(String)
    disabled = Column(Boolean, default=False)


class UserData(Base):
    __tablename__ = "user_data"

    userId = Column(Integer, primary_key=True)
    personId = Column(Integer)
    dni = Column(String)
    firstName = Column(String)
    lastName = Column(String)
    role = Column(String)
    mail = Column(String)
    username = Column(String)
    disabled = Column(Boolean)

Base.metadata.create_all(bind=engine)


def create_user(user: UserDB, db: Session):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user.id


def get_all_users(db: Session):
    users = db.query(UserDB).all()
    return users


def find_user_by_id(id: int, db: Session):
    user = db.query(UserDB).get(id)
    return user

'''
def get_user(username: str, db: Session):
    if username in db:
        user = db.query(UserDB).filter(username == UserDB.username)        
        return 
'''