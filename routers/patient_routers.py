from fastapi import APIRouter, Depends, HTTPException
from db.db_connection import get_db
from sqlalchemy.orm import Session

from db.person_db import PersonDB
from db.patient_db import PatientDB, PatientData
from db.history_db import HistoryDB
from db.treatment_db import TreatmentDB
from db.address_db import AddressDB, PhoneDB
from db.representative_db import RepresentativeDB
import db.person_db, db.patient_db, db.address_db, db.representative_db

from models.person_models import NewPerson
from models.patient_models import NewPatient


router = APIRouter()


@router.get("/patients")
async def get_patients(db: Session = Depends(get_db)):
    patients = db.query(PatientDB).all()
    print(patients)
    return patients 


@router.get("/patients-data")
async def get_patients_data(db: Session = Depends(get_db)):
    patients_data = db.query(PatientData).all()
    return patients_data 


@router.get("/patient-data/{id}")
async def get_patient(id: int, db: Session = Depends(get_db)):
    patient_data = db.query(PatientData).get(id)
    if patient_data == None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient_data


@router.get("/patient/{id}")
async def get_patient(id: int, db: Session = Depends(get_db)):
    patient = db.query(PatientDB).get(id)
    if patient == None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.post("/patient")
async def save_patient (patient: NewPatient, database: Session = Depends(get_db)):   

    #Crea una persona que corresponde al paciente    
    person_in = {
        "dni": patient.dni,
        "firstName": patient.firstName,
        "lastName": patient.lastName,
        "mail": patient.mail
    }

    new_person = PersonDB(**person_in)
    person_id = db.person_db.create_person(new_person, database)


    #Crea un paciente y lo asigna a la persona creada anteriormente 
    patient_in = {
        "personId": person_id,
        "birthday": patient.birthday,
        "sex": patient.sex,
        "country": patient.country,
        "civilState": patient.civilState,
        "schoolGrade": patient.schoolGrade,
        "schoolLevel": patient.schoolLevel,
        "occupation": patient.occupation,
        "salary": patient.salary,
        "isInsured": patient.isInsured,
        "provider": patient.provider,
        "healthCard": patient.healthCard,
        "religion": patient.religion,
        "language": patient.language,
        "bloodType": patient.bloodType,
        "rh": patient.rh,
    }
    
    new_patient = PatientDB(**patient_in)
    patient_id = db.patient_db.create_patient(new_patient, database)    


    #Crea una historia clínica y la asigna al paciente
    history_in = {
        "patientId": patient_id,
        "code": new_person.dni
    }
    new_history = HistoryDB(**history_in)
    history_id = db.history_db.create_history(new_history, database)


    #Crea un tratamiento y lo asigna a la hisoria
    treatment_in = {
        "historyId": history_id,
        "code": new_history.code + 'R0',
        "isActive": True
    }
    new_treatment = TreatmentDB(**treatment_in)
    treatment_id = db.treatment_db.add_treatment(new_treatment, database)

    #Crea una dirección y la asigna a la persona del paciente
    address_in = {
        "personId": person_id,
        "street": patient.address.street,
        "number": patient.address.number,
        "crossStreetBackward": patient.address.crossStreetBackward,
        "crossStreetForward": patient.address.crossStreetForward,
        "suburb": patient.address.suburb,
        "postalCode": patient.address.postalCode,
        "municipality": patient.address.municipality,
        "state": patient.address.state        
    }

    new_address = AddressDB(**address_in)
    db.address_db.add_address(new_address, database)    



    #Crea dos teléfonos y los asigna a la persona del paciente
    phone1_in = {
        "personId": person_id,        
        "number": patient.phone1.number
    }

    new_phone = PhoneDB(**phone1_in)
    db.address_db.add_phone(new_phone, database)    


    if patient.phone2 is not None:
        phone2_in = {
            "personId": person_id,        
            "number": patient.phone2.number
        }

        new_phone = PhoneDB(**phone2_in)
        db.address_db.add_phone(new_phone, database)        



    #Crea una persona que corresponde al representante  
    person_in = {
        "dni": patient.representative.dni,
        "firstName": patient.representative.firstName,
        "lastName": patient.representative.lastName,
        "mail": patient.representative.mail
    }
    new_person = PersonDB(**person_in)
    person_id = db.person_db.create_person(new_person, database)


    #Crea un representante y lo asigna a la persona creada anteriormente, y al paciente creado antes
    representative_in = {
        "personId": person_id,
        "patientId": patient_id,
        "birthday": patient.representative.birthday,
        "occupation": patient.representative.occupation,
        "relationship": patient.representative.relationship
    }

    new_representative = RepresentativeDB(**representative_in)
    db.representative_db.create_representative(new_representative, database)


    #Crea una dirección y la asigna a la persona del representante
    address_in = {
        "personId": person_id,
        "street": patient.representative.address.street,
        "number": patient.representative.address.number,
        "crossStreetBackward": patient.representative.address.crossStreetBackward,
        "crossStreetForward": patient.representative.address.crossStreetForward,
        "suburb": patient.representative.address.suburb,
        "postalCode": patient.representative.address.postalCode,
        "municipality": patient.representative.address.municipality,
        "state": patient.representative.address.state        
    }

    new_address = AddressDB(**address_in)
    db.address_db.add_address(new_address, database)


    #Crea un teléfono y lo asigna a la persona del representante
    phone_in = {
        "personId": person_id,        
        "number": patient.representative.phone.number
    }

    new_phone = PhoneDB(**phone_in)
    db.address_db.add_phone(new_phone, database)


    return {"message": "Patient created succesfully."}



@router.delete("/patient/{id}")
async def delete_patient(id: int, db: Session = Depends(get_db)):
    db.query(PatientDB).filter(PatientDB.id==id).delete()
    db.commit()
    return {"message": "Patient deleted succesfully"}