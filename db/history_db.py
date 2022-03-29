from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Session
import datetime
from db.db_connection import Base, engine


class HistoryDB(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    patientId = Column(Integer, ForeignKey('patient.id'))
    code = Column(String)
    creationDate = Column(DateTime, default=datetime.datetime.utcnow)


Base.metadata.create_all(bind=engine)


def create_history(history: HistoryDB, db: Session):
    db.add(history)
    db.commit()
    db.refresh(history)
    return history.id