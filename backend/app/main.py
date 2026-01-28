from fastapi import FastAPI, HTTPException, Depends
from app.schemas import ReminderCreate, ReminderUpdate, ReminderRead
from db.deps import get_db
from sqlalchemy.orm import Session
from db import crud
from typing import List
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone

# Automatic db creation
from db.base import Base, engine
Base.metadata.create_all(bind=engine)

# Async functions need async sessions

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:5173"
]

# Creating midddleware for Cross-Origin Resource Sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get('/')
async def index():
    return {"message": "App is working"}


@app.get('/reminders', response_model=List[ReminderRead], description="Returns all reminders in the app")
# Get all reminders
async def all_reminders(db: Session = Depends(get_db)):
    reminders = crud.get_all_reminders(db)
    if not reminders:
        return []
    return reminders


@app.post('/create', response_model=ReminderRead, description="Create reminder")
# Create reminder
async def create_reminder(
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


@app.get('/reminders/{id}', response_model=ReminderRead, description="Get reminders by its ID")
# Get specific reminder
async def get_reminder(id: int, db: Session = Depends(get_db)):
    reminder = crud.get_reminder(db, id)
    if not reminder:
        raise HTTPException(status_code=404, detail="Object was not found")
    return reminder


@app.put('/reminders/{id}', response_model=ReminderRead, description="Edit reminder")
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


@app.delete('/reminders/{id}', description="Delete reminder by its ID")
# Delete reminder
async def delete_reminder(id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_reminder(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Object was not found")

    return deleted


@app.delete('/reminders', description="Delete all reminders")
# Delete all reminders
async def delete_all_reminders(db: Session = Depends(get_db)):
    deleted_reminders = crud.delete_all(db)
    if not deleted_reminders:
        return {'message': 'No reminders to delete'}

    return deleted_reminders
