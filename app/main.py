from fastapi import FastAPI, HTTPException, Depends
from app.schemas import ReminderCreate, ReminderUpdate, ReminderRead
from db.deps import get_db
from sqlalchemy.orm import Session
from db import crud
from typing import List
from .send_mail import send_mail


app = FastAPI()
mail_receiver = 'pythoneqq36@gmail.com'

@app.get('/')
async def index():
    return {"message": "App is working"}


@app.get('/reminders', response_model=List[ReminderRead])
# Get all reminders
async def all_reminders(db: Session = Depends(get_db)):
    reminders = crud.get_all_reminders(db)
    if not reminders:
        return []
    return reminders


@app.post('/create', response_model=ReminderRead)
# Create reminder
async def create_reminder(
    reminder: ReminderCreate, 
    db: Session = Depends(get_db)
):
    new_reminder = crud.create_reminder(
        db,
        title=reminder.title,
        description=reminder.description,
        due_to=reminder.due_to
    )
    
    send_mail(
        mail_receiver, 
        f"New reminder added: {new_reminder.title}",
        f"New reminder was added to you list: \n{new_reminder.title}\n{new_reminder.description}"
        )
    return new_reminder


@app.get('/reminders/{id}', response_model=ReminderRead)
# Get specific reminder
async def get_reminder(id: int, db: Session = Depends(get_db)):
    reminder = crud.get_reminder(db, id)
    if not reminder:
        raise HTTPException(status_code=404, detail="Object was not found")
    return reminder


@app.put('/reminders/{id}', response_model=ReminderRead)
# Update reminder values
async def update_reminder(
    id: int, 
    reminder: ReminderUpdate, 
    db: Session = Depends(get_db)
):
    updated_reminder = crud.update_reminder(db, id, reminder)
    
    if not updated_reminder:
        raise HTTPException(status_code=404, detail="Object was not found")

    return updated_reminder


@app.delete('/reminders/{id}')
# Delete reminder
async def delete_reminder(id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_reminder(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Object was not found")
    
    return deleted