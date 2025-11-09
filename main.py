from fastapi import FastAPI, HTTPException
from schemas import Reminder

app = FastAPI()

reminders = []


@app.get('/')
async def all_reminders():
    return reminders


@app.post('/add')
async def add_reminder(reminder: Reminder):
    reminder.id = len(reminders) + 1
    reminders.append(reminder)
    return {"message": "Succesfully added", "reminder": reminder}


@app.delete('/delete/{reminder_id}')
async def delete_reminder(reminder_id: int):
    for r in reminders:
        if reminder_id == r.id:
            reminders.remove(r)
            return {"message": "Reminder succesfully deleted"}

    raise HTTPException(status_code=404, detail="Reminder not found")