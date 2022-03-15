from fastapi import APIRouter, Depends, HTTPException
from db.db_connection import get_db
from sqlalchemy.orm import Session

from db.representative_db import RepresentativeDB, RepresentativeData

router = APIRouter()


@router.get("/representative-data/{id}")
async def get_representative(id: int, db: Session = Depends(get_db)):

    representative = db.query(RepresentativeData).filter(RepresentativeData.patientId == id).first()
    if representative == None:
        raise HTTPException(status_code=404, detail="Person not found")
    return representative