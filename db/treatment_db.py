from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Session
import datetime
from db.db_connection import Base, engine


class TreatmentDB(Base):
    __tablename__ = "treatment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    historyId = Column(Integer, ForeignKey('history.id'))
    code = Column(String)
    entryDate = Column(DateTime, default=datetime.datetime.utcnow)
    wayOutDate = Column(DateTime)
    isActive = Column(Boolean)


Base.metadata.create_all(bind=engine)


def add_treatment(treatment: TreatmentDB, db: Session):
    db.add(treatment)
    db.commit()
    db.refresh(treatment)
    return treatment.id


#def get_patient_treatments(patient_id: int, db: Session):
#    db.query(TreatmentDB).filter()

def find_treatments(id: int, db: Session):
    #treatments = db.query(TreatmentDB).filter(id == TreatmentDB.historyId).order_by(TreatmentDB.entryDate).all()
    treatments = db.query(TreatmentDB).filter(TreatmentDB.historyId == id).order_by(TreatmentDB.entryDate).all()
    print(treatments[0].entryDate)
    return treatments