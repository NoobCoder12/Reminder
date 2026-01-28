# Reminder App

A full-stack reminder application that allows users to create tasks with email notifications sent before deadlines.\

App was built with:
 - **FastAPI** (backend API)
 - **Celery + Celery Beat** (background task scheduling)
 - **SQLite / SQLAlchemy** (database)
 - **React** (frontend)
 - **Docker** 
 - **Email notifications (SMTP / Gmail)**

 ---

## Features

- Create, edit, delete reminders
- Choose alert type:
    - 15 minutes before deadline
    - 1 hour before deadline
    - 1 day before deadline
- Email notification sent automatically
- Timezone handling
- Frontend displays user's local timezone
- Background tasks handled by Celery

