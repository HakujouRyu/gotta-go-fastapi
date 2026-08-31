import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import StaticPool

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

# SQLite (used by default in tests, see tests/conftest.py) needs a couple of
# non-default knobs to behave like a normal single database inside a process:
# - check_same_thread=False: FastAPI runs sync path operations in a worker
#   thread, so the connection must be usable outside the thread that made it.
# - StaticPool for :memory: DBs: without it, every checked-out connection is
#   its own empty in-memory database and tables "disappear" between queries.
connect_args = {}
engine_kwargs = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False
    if ":memory:" in DATABASE_URL:
        engine_kwargs["poolclass"] = StaticPool

engine = create_engine(DATABASE_URL, connect_args=connect_args, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
