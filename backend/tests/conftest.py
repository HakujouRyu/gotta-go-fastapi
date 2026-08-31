import os

# Default to a fast, dependency-free in-memory SQLite DB so `pytest` works with
# zero setup. Set DATABASE_URL yourself (e.g. to the docker-compose Postgres, or
# what CI uses) to run the suite against Postgres instead — useful before
# relying on any Postgres-specific behavior. Must run before `app.common.database`
# is imported anywhere, since it reads DATABASE_URL at import time.
os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import common  # noqa: F401  # Registers models with Base.metadata
from app.common.database import Base, SessionLocal, engine, get_db
from app.main import app


@pytest.fixture(scope="function")
def db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db_session = SessionLocal()

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    yield db_session

    db_session.close()
    app.dependency_overrides.clear()


@pytest.fixture
def client(db: Session):
    return TestClient(app)
