from celery import Celery
from celery.signals import worker_process_init
from db.base import engine

celery = Celery(
    "tasks",
    broker="redis://redis_container:6379/0",
    backend="redis://redis_container:6379/0"
)

celery.conf.timezone = "Europe/Warsaw"

celery.conf.beat_schedule = {
    "check_tasks_every_minute": {
        "task": "app.tasks.check_reminders",    # Name of task
        "schedule": 10.0    # Check every minute
    }
}

from app.tasks import check_reminders


@worker_process_init.connect
def setup_db_connection(**kwargs):  # Use **kwargs for signals
    """Dispose engine connections after worker process fork"""
    
    print("🔧 Worker initialized - disposing SQLAlchemy engine")
    engine.dispose()    # Closes parent connection, no for conflicts
