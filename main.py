from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware


from routers.patient_routers import router as router_patient
from routers.person_routers import router as router_person
from routers.representative_routers import router as router_representative
from routers.user_routers import router as router_user
from routers.form_routers import router as router_form
from routers.treatment_routers import router as router_treatment
from routers.address_routers import router as router_address
from routers.disease_routers import router as router_disease

api = FastAPI()


api.include_router(router_patient)
api.include_router(router_person)
api.include_router(router_representative)
api.include_router(router_user)
api.include_router(router_form)
api.include_router(router_treatment)
api.include_router(router_address)
api.include_router(router_disease)

origins = [
    "http://localhost:8080", "https://auriga-web.netlify.app"
]

api.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

@api.get("/")
async def hola_mundo():
    return { "mensaje": "Api funcionando..."} 