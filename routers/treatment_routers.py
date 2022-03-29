from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.db_connection import get_db
from db.treatment_db import TreatmentDB
import db.treatment_db


router = APIRouter()


#@router.get("patient-treatments")
#async def get_treatments_by_patient_id(id: int, database: Session = Depends(get_db)):
#   return 


@router.get("/patient-treatments/{id}")
async def get_treatments_by_history_id(id: int, database: Session = Depends(get_db)):
    return db.treatment_db.find_treatments(id, database)