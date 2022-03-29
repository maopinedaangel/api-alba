from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session
from db.db_connection import Base, engine


class UserDB(Base):
    __tablename__ = "auriga_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    personId = Column(Integer, ForeignKey('person.id'))
    role = Column(String)
    username = Column(String)
    password = Column(String)


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