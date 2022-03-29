from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Session
import datetime
from db.db_connection import Base, engine


class FormTypeDB(Base):
    __tablename__ = "form_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    allowMultiple = Column(Boolean)


class FormDB(Base):
    __tablename__ = "form"

    id = Column(Integer, primary_key=True, autoincrement=True)
    treatmentId = Column(Integer, ForeignKey('treatment.id'))
    creationDate = Column(DateTime, default=datetime.datetime.utcnow)
    formTypeId = Column(Integer, ForeignKey('form_type.id'))
    data = Column(JSONB)
    file = Column(String)
    userId = Column(Integer, ForeignKey('auriga_user.id'))


class FormList(Base):
    __tablename__ = "form_list"

    id = Column(Integer, primary_key=True)
    treatmentId = Column(Integer)
    patientId = Column(Integer)
    creationDate = Column(DateTime)
    formType = Column(String)

Base.metadata.create_all(bind=engine)


def get_all_form_types(db: Session):
    return db.query(FormTypeDB).all()


def create_form_type(form_type: FormTypeDB, db: Session):
    db.add(form_type)
    db.commit()
    db.refresh(form_type)
    return form_type.id


def get_all_forms(db: Session):
    forms = db.query(FormDB).order_by(FormDB.creationDate).all()
    return forms


def find_forms_by_treatment_id(id: int, db: Session):
    forms = db.query(FormList).filter(id == FormList.treatmentId).all()
    return forms


def find_form_by_id(id: int, db: Session):
    return db.query(FormDB).get(id)
  

def save_form(form: FormDB, db: Session):
    db.add(form)
    db.commit()
    db.refresh(form)
    return form.id