from sqlalchemy import Column, Integer, DateTime, String
from datetime import datetime, timezone
from .base import Base, engine


class Reminder(Base):
    __tablename__ = "reminders"     # table name in db

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    due_to = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    times_alert_sent = Column(Integer, default=0, nullable=False)


Base.metadata.create_all(bind=engine)   # Create table in database, error otherwise
