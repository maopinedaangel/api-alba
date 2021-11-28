from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

api = FastAPI()


origins = [
    "http://localhost:8080", "https://r-store.herokuapp.com", "https://albastore.netlify.app"
]

api.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

@api.get("/")
async def hola_mundo():
    return { "mensaje": "Api Alba funcionando..."} 