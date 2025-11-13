from pydantic import BaseModel, field_validator
from datetime import datetime


class ReminderCreate(BaseModel):
    title: str
    description: str
    due_to: str

    @field_validator('due_to', mode='before')
    def check_date(cls, value):
        try:
            datetime.strptime(value, "%d-%m-%Y %H:%M")
        except ValueError:
            raise ValueError("Field should be filled in dd-mm-yyyy hh:mm format")
        return value


class ReminderUpdate(BaseModel):
    id: int | None = None
    title: str | None = None
    description: str | None = None
    due_to: str | None = None

    @field_validator('due_to', mode='before')
    def check_date(cls, value):
        if value is None:
            return value
        try:
            datetime.strptime(value, "%d-%m-%Y %H:%M")
        except ValueError:
            raise ValueError("Field should be filled in dd-mm-yyyy hh:mm format")
        return value


class ReminderRead(BaseModel):
    id: int
    title: str
    description: str
    due_to: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime("%d-%m-%Y %H:%M")
        }
        
        
class EmailSchema(BaseModel):
    to: str
    subject: str
    body: str