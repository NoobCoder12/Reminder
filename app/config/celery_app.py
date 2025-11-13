from celery import Celery

celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery.conf.timezone = "Europe/Warsaw"

celery.conf.beat_schedule = {
    "check_tasks_every_minute": {
        "task": "app.tasks.check_reminders",    # Name of task
        "schedule": 60.0    # Check every minute
    }
}