from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATABASE_URL = f"sqlite:///{ROOT}/test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})     # If not False there would be an error while doing multiple threads
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
