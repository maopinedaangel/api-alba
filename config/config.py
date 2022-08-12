from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    admin_email: str
    password_email: str
    icd_client_id: str
    icd_client_Secret: str 

    class Config:
        env_file = ".env"


settings = Settings()