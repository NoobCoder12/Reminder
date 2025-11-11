from .base import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db    # database works as long as request
    finally:
        db.close()      # closed when request ends