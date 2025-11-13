from app.config.celery_app import celery

@celery.task
def check_reminders():
    