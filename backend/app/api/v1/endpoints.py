from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import ReminderCreate, ReminderRead, ReminderUpdate
from db import crud
from db.deps import get_db

router = APIRouter()

@router.get(
    '/reminders',
    response_model=List[ReminderRead],
    description="Returns all reminders in the app"
)
# Get all reminders
def all_reminders(db: Session = Depends(get_db)):
    reminders = crud.get_all_reminders(db)
    if not reminders:
        return []
    return reminders


@router.post(
    '/create',
    response_model=ReminderRead,
    description="Create reminder"
)
# Create reminder
def create_reminder(
    reminder: ReminderCreate,
    db: Session = Depends(get_db)
):

    new_reminder = crud.create_reminder(
        db,
        title=reminder.title,
        description=reminder.description,
        due_to=reminder.due_to,
        email=reminder.email,
        alert_type=reminder.alert_type
    )
    return new_reminder


@router.get(
    '/reminders/{id}',
    response_model=ReminderRead,
    description="Get reminders by its ID"
)
# Get specific reminder
def get_reminder(id: int, db: Session = Depends(get_db)):
    reminder = crud.get_reminder(db, id)
    if not reminder:
        raise HTTPException(status_code=404, detail="Object was not found")
    return reminder


@router.put(
    '/reminders/{id}',
    response_model=ReminderRead,
    description="Edit reminder"
)
# Update reminder values
def update_reminder(
    id: int,
    reminder: ReminderUpdate,
    db: Session = Depends(get_db)
):
    updated_reminder = crud.update_reminder(db, id, reminder)

    if not updated_reminder:
        raise HTTPException(status_code=404, detail="Object was not found")

    return updated_reminder


@router.delete('/reminders/{id}', description="Delete reminder by its ID")
# Delete reminder
def delete_reminder(id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_reminder(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Object was not found")

    return deleted


@router.delete('/reminders', description="Delete all reminders")
# Delete all reminders
def delete_all_reminders(db: Session = Depends(get_db)):
    deleted_reminders = crud.delete_all(db)
    if not deleted_reminders:
        return {'message': 'No reminders to delete'}

    return deleted_reminders
