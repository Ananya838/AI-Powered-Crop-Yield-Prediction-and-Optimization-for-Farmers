import os
import tempfile
from pathlib import Path

test_db_path = Path(tempfile.gettempdir()) / "crop_ai_test.db"
if test_db_path.exists():
    test_db_path.unlink()

os.environ.setdefault("DATABASE_URL", f"sqlite:///{test_db_path}")
os.environ.setdefault("SECRET_KEY", "test-secret")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from app.core.database import Base, engine, SessionLocal
from app.core.security import create_access_token, get_password_hash
from app.main import app
from app.models.user import User


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def seeded_user(db_session):
    existing = db_session.query(User).filter(User.phone == "9999999999").first()
    if existing:
        return existing

    user = User(
        full_name="Test Farmer",
        phone="9999999999",
        language="en",
        hashed_password=get_password_hash("password123"),
        is_admin=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture()
def auth_token(seeded_user):
    return create_access_token(seeded_user.id)
