from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Literal


class ReminderCreate(BaseModel):
    title: str
    description: str
    due_to: datetime
    email: str
    alert_type: Literal["minutes", 'hours', "days"]

    @field_validator('due_to', mode='before')
    def check_date(cls, value):
        if isinstance(value, datetime):
            return value
        try:
            return datetime.strptime(value, "%d-%m-%Y %H:%M")
        except ValueError:
            raise ValueError("Field should be filled in dd-mm-yyyy hh:mm format")


class ReminderUpdate(BaseModel):
    id: int | None = None       # Field optional
    title: str | None = None
    description: str | None = None
    due_to: datetime | None = None
    email: str | None = None

    @field_validator('due_to', mode='before')
    def check_date(cls, value):
        if value is None or isinstance(value, datetime):
            return value
        try:
            return datetime.strptime(value, "%d-%m-%Y %H:%M")
        except ValueError:
            raise ValueError("Field should be filled in dd-mm-yyyy hh:mm format")
        


class ReminderRead(BaseModel):
    id: int
    title: str
    description: str
    due_to: datetime
    email: str

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime("%d-%m-%Y %H:%M")
        }


class EmailSchema(BaseModel):
    to: str
    subject: str
    body: str
