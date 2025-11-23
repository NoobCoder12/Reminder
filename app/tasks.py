from app.config.celery_app import celery
from db.crud import get_all_reminders
from datetime import datetime
from app.send_mail import send_mail
import os
from db.base import SessionLocal
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


RECEIVER = os.environ.get("RECEIVER_MAIL")
DIFFERENCE_IN_DAYS = 1


@celery.task
def check_reminders():
    db = SessionLocal()
    try:
        reminders = get_all_reminders(db)

        if not reminders:
            logger.info("No reminders in database")

        for r in reminders:
            delta = r.due_to - datetime.now()
            if 0 <= delta.days <= DIFFERENCE_IN_DAYS and r.times_alert_sent < 3:
                send_mail(
                    RECEIVER,
                    "YOUR TASK IS DUE TO TOMORROW",
                    f"It's your reminder! Don't forget about {r.title}! Deadline expires tomorrow. Good luck!")
                r.times_alert_sent += 1
        db.commit()

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)  # exc_info adds stack trace
        db.rollback()   # In case of error changes are not saved

    finally:
        db.close()
