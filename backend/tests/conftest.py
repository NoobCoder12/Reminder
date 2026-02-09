import pytest
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from db.base import Base
from fastapi.testclient import TestClient
from app.main import app
from db.deps import get_db

# After running pytest this file is saved in memory. In case of any 'client' mentions it checkes the name here - Dependency Injection

# Database for testing
TEST_DATABASE_URL = "sqlite:///./test_api.db"


@pytest.fixture  # Pytest prepare for other functions
def test_db() -> Session:
    '''
    Creates clean database for each test.
    After completing database is removed.
    '''

    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})    # Create engine in RAM

    from db.models import Reminder  # noqa: F401, import for Base

    Base.metadata.create_all(bind=engine)   # Creating db

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # Connections factory
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)  # Clear after test


@pytest.fixture
def client(test_db: Session) -> TestClient:
    """
    TestClient FastAPI with test database.
    Used to test endpoints, simulates user's action.
    """
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db  # Switching database to test unit

    with TestClient(app) as c:
        yield c     # Creating client for an action

    app.dependency_overrides.clear()    # Switching back to database


@pytest.fixture
def reminder_payload():
    return {
        "title": 'Laundry',
        "description": "Remember about laundry",
        "due_to": "24-12-2026 12:00",
        "email": "test@example.com",
        "alert_type": "minutes"
    }
