from sqlalchemy.orm import Session
from . import models
from datetime import datetime
from app.schemas import ReminderUpdate


# Read all
def get_all_reminders(db: Session):
    return db.query(models.Reminder).all()


# Create reminder
def create_reminder(db: Session, title: str, description: str, due_to: str, email: str):
    try:
        due_to_dt = datetime.strptime(due_to, "%d-%m-%Y %H:%M")
    except ValueError:
        raise ValueError("due_to must be in format DD-MM-YYYY HH:MM")

    reminder = models.Reminder(title=title, description=description, due_to=due_to_dt, email=email)
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder


# Read specific reminder
def get_reminder(db: Session, id: int):
    return db.get(models.Reminder, id)


# Update reminder
def update_reminder(db: Session, id: int, update_data: ReminderUpdate):

    reminder = db.get(models.Reminder, id)

    if not reminder:
        return None

    update_dict = update_data.model_dump(exclude_unset=True)
    
    for field, value in update_dict.items():
        if field == 'due_to':
            value = datetime.strptime(value, "%d-%m-%Y %H:%M")
        setattr(reminder, field, value)

    db.commit()
    db.refresh(reminder)
    return reminder


# Delete reminder
def delete_reminder(db: Session, id: int):
    reminder = db.get(models.Reminder, id)
    if not reminder:
        return None

    db.delete(reminder)
    db.commit()
    return reminder


# Delete all reminders
def delete_all(db: Session):
    deleted_reminders = db.query(models.Reminder).delete()

    db.commit()
    db.expire_all()     # New GET will get updated rows

    if not deleted_reminders:
        return None

    return deleted_reminders
