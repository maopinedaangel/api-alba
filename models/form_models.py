from pydantic import BaseModel, Json
from typing import Optional


class FormTypeIn(BaseModel):
    name: str
    allowMultiple: bool



class FormIn(BaseModel):
    treatmentId: int
    formTypeId: int
    data: Json
    file: Optional[str]
    userId: int

