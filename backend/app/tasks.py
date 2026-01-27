from app.config.celery_app import celery
from db.crud import get_all_reminders
from datetime import datetime, timezone
from app.send_mail import send_mail
import os
from db.base import SessionLocal
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


RECEIVER = os.environ.get("RECEIVER_MAIL")

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR

# Only one should be true
ALERT_MINUTES = True
ALERT_HOURS = False
ALERT_DAYS = False

# CONSIDER ADDING FLAGS FOR HOURS, DAYS, MINUTES FROM FRONTEND

ALERT_THRESHOLD_SECONDS = None 

if ALERT_MINUTES:
    ALERT_THRESHOLD_SECONDS = 30 * MINUTE    # 30 minutes before
    subject = f"YOUR TASK IS DUE IN {ALERT_THRESHOLD_SECONDS // MINUTE} minutes"
elif ALERT_HOURS:
    ALERT_THRESHOLD_SECONDS = 1 * HOUR   # 1 hour before
    subject = f"YOUR TASK IS DUE IN {ALERT_THRESHOLD_SECONDS // HOUR} hours"
elif ALERT_DAYS:
    ALERT_THRESHOLD_SECONDS = 2 * DAY    # 2 days before
    subject = f"YOUR TASK IS DUE IN {ALERT_THRESHOLD_SECONDS // DAY} days"


@celery.task
def check_reminders():
    db = SessionLocal()
    try:
        logger.info(f"🔍 Database URL: {db.bind.url}")
        # db.expire_all()
        reminders = get_all_reminders(db)

        if not reminders:
            logger.info("No reminders in database")

        now = datetime.now(timezone.utc)

        for r in reminders:
            delta = r.due_to - now
            receiver = r.email
            seconds_left = delta.total_seconds()
            print(f"ZOSTAŁO {seconds_left}, CZAS TO: {ALERT_THRESHOLD_SECONDS}")
            if seconds_left <= 0:
                print(f"Expired - skipping task {r.title}")
                continue
            elif 0 <= seconds_left <= ALERT_THRESHOLD_SECONDS and r.times_alert_sent < 3:
                send_mail(
                    receiver,
                    subject,
                    f"It's your reminder! Don't forget about {r.title}! Deadline expires soon. Good luck!")
                r.times_alert_sent += 1
        db.commit()

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)  # exc_info adds stack trace
        db.rollback()   # In case of error changes are not saved

    finally:
        db.close()
