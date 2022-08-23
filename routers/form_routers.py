from fastapi import APIRouter, Depends, HTTPException
from db.db_connection import get_db
from sqlalchemy.orm import Session

from db.form_db import FormDB, FormTypeDB
from models.form_models import FormIn, FormTypeIn
import db.form_db


router = APIRouter()


@router.get("/form-types")
async def get_form_types(database: Session = Depends(get_db)):
    return db.form_db.get_all_form_types(database)


@router.post("/form-type")
async def new_form_type(form_type: FormTypeIn, database: Session = Depends(get_db)):
    form_type_in = {
        "name": form_type.name,
        "allowMultiple": form_type.allowMultiple
    }
    new_form_type = FormTypeDB(**form_type_in)
    db.form_db.create_form_type(new_form_type, database)
    return { "message": "Form type created successfully"}


@router.get("/forms-all")
async def get_forms(database: Session = Depends(get_db)):
    return db.form_db.get_all_forms(database)


@router.get("/forms-data")
async def get_forms_data(database: Session = Depends(get_db)):
    return db.form_db.get_all_forms_data(database)


@router.get("/forms")
async def get_forms_by_treatment_id(id: int, database: Session = Depends(get_db)):
    return db.form_db.find_forms_by_treatment_id(id, database)

@router.get("/form/{id}")
async def get_form_by_id(id: int, database: Session = Depends(get_db)):
    return db.form_db.find_form_by_id(id, database)



@router.post("/form")
async def save_form(form: FormIn, database: Session = Depends(get_db)):
    form_in = {
        "treatmentId": form.treatmentId,
        "formTypeId": form.formTypeId,
        "data": form.data,
        "file": form.file,
        "userId": form.userId
    }
    new_form = FormDB(**form_in)
    db.form_db.save_form(new_form, database)
    return { "message": "For created successfully" }