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

# # Only one should be true
# ALERT_MINUTES = False
# ALERT_HOURS = False
# ALERT_DAYS = False


@celery.task
def check_reminders():
    db = SessionLocal()
    try:
        logger.info(f"Database URL: {db.bind.url}")
        # db.expire_all()
        reminders = get_all_reminders(db)

        if not reminders:
            logger.info("No reminders in database")
            return

        now = datetime.now(timezone.utc)
        
        for r in reminders:
            
            ALERT_THRESHOLD_SECONDS = None 
            
            # In case of wrong data
            if r.alert_type not in ("minutes", "hours", "days"):
                logger.warning(f"Unknown alert_type for reminder {r.id}")
                continue
            
            if r.alert_type == 'minutes':
                ALERT_THRESHOLD_SECONDS = 15 * MINUTE    # 15 minutes before
                subject = f"YOUR TASK IS DUE IN {ALERT_THRESHOLD_SECONDS // MINUTE} MINUTES"
            elif r.alert_type == 'hours':
                ALERT_THRESHOLD_SECONDS = 1 * HOUR   # 1 hour before
                subject = f"YOUR TASK IS DUE IN {ALERT_THRESHOLD_SECONDS // HOUR} HOUR"
            elif r.alert_type == 'days':
                ALERT_THRESHOLD_SECONDS = 1 * DAY    # 1 days before
                subject = f"YOUR TASK IS DUE IN {ALERT_THRESHOLD_SECONDS // DAY} DAY"
            
            # Making date aware
            due_to = r.due_to
            
            # due_to is stored in DB as UTC-naive datetime
            if due_to.tzinfo is None:
                due_to = due_to.replace(tzinfo=timezone.utc)
                
            delta = due_to - now
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
