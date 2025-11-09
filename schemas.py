from pydantic import BaseModel, field_validator
from datetime import datetime
from fastapi import HTTPException


class Reminder(BaseModel):
    id: int
    title: str
    description: str
    due_to: str
    
    @field_validator('due_to', mode='before')
    def check_date(cls, value):
        try:
            datetime.strptime(value, "%d-%m-%Y %H:%M")
        except ValueError:
            raise HTTPException(status_code=422, detail="Field should be filled in dd-mm-yyyy hh:mm format")
        return value