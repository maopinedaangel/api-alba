from fastapi import APIRouter, Depends, HTTPException
from db.db_connection import get_db
from sqlalchemy.orm import Session

from db.person_db import PersonDB
from db.patient_db import PatientDB, PatientData
from db.address_db import AddressDB, PhoneDB
from db.representative_db import RepresentativeDB

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

'''
@router.post("/patient")
async def save_patient (patient: NewPatient, db: Session = Depends(get_db)):
    person_in = {
        "dni": patient.dni,
        "firstName": patient.firstName,
        "lastName": patient.lastName
    }
    new_person = PersonDB(**person_in)
    print(new_person)

    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    print(new_person)

    patient_in = {
        "personId": new_person.id,
        "birthday": patient.birthday,
        "sex": patient.sex,
        "country": patient.country,
        "civilState": patient.civilState,
        "schoolGrade": patient.schoolGrade,
        "occupation": patient.occupation,
    }
    
    new_patient = PatientDB(**patient_in)
    print(new_patient)

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return {"message": "Patiente created succesfully."}
'''

@router.post("/patient")
async def save_patient (patient: NewPatient, db: Session = Depends(get_db)):

    #Crea una persona que corresponde al paciente    
    person_in = {
        "dni": patient.dni,
        "firstName": patient.firstName,
        "lastName": patient.lastName,
        "mail": patient.mail
    }

    new_person = PersonDB(**person_in)
    print(new_person)

    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    print(new_person)


    #Crea un paciente y lo asigna a la persona creada anteriormente 
    patient_in = {
        "personId": new_person.id,
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
    print(new_patient)

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)


    #Crea una dirección y la asigna a la persona del paciente
    address_in = {
        "personId": new_person.id,
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
    print(new_address)

    db.add(new_address)
    db.commit()
    db.refresh(new_address)

    #Crea dos teléfonos y los asigna a la persona del paciente
    phone1_in = {
        "personId": new_person.id,        
        "number": patient.phone1.number
    }

    new_phone = PhoneDB(**phone1_in)

    db.add(new_phone)
    db.commit()
    db.refresh(new_phone)

    if patient.phone2 is not None:
        phone2_in = {
            "personId": new_person.id,        
            "number": patient.phone2.number
        }

        new_phone = PhoneDB(**phone2_in)

        db.add(new_phone)
        db.commit()
        db.refresh(new_phone)   


    #Crea una persona que corresponde al representante  
    person_in = {
        "dni": patient.representative.dni,
        "firstName": patient.representative.firstName,
        "lastName": patient.representative.lastName,
        "mail": patient.representative.mail
    }
    new_person = PersonDB(**person_in)
    print(new_person)

    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    print(new_person)


    #Crea un representante y lo asigna a la persona creada anteriormente, y al paciente creado antes
    representative_in = {
        "personId": new_person.id,
        "patientId": new_patient.id,
        "birthday": patient.representative.birthday,
        "occupation": patient.representative.occupation,
        "relationship": patient.representative.relationship
    }

    new_representative = RepresentativeDB(**representative_in)
    print(new_representative)

    db.add(new_representative)
    db.commit()
    db.refresh(new_representative)    


    #Crea una dirección y la asigna a la persona del representante
    address_in = {
        "personId": new_person.id,
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
    print(new_address)

    db.add(new_address)
    db.commit()
    db.refresh(new_address)

    #Crea un teléfono y lo asigna a la persona del representante
    phone_in = {
        "personId": new_person.id,        
        "number": patient.representative.phone.number
    }

    new_phone = PhoneDB(**phone_in)

    db.add(new_phone)
    db.commit()
    db.refresh(new_phone)


    return {"message": "Patient created succesfully."}



@router.delete("/patient/{id}")
async def delete_patient(id: int, db: Session = Depends(get_db)):
    db.query(PatientDB).filter(PatientDB.id==id).delete()
    db.commit()
    return {"message": "Patient deleted succesfully"}