import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import StaticPool

load_dotenv()

# DB_ENGINE picks which database backend to use ("postgres" or "sqlite"); see
# .env.example. An explicit DATABASE_URL always wins over DB_ENGINE - that's how
# tests (see tests/conftest.py) and CI pin an in-memory/real Postgres URL without
# needing to care about DB_ENGINE at all.
if "DATABASE_URL" in os.environ:
    DATABASE_URL = os.environ["DATABASE_URL"]
else:
    DB_ENGINE = os.environ.get("DB_ENGINE", "postgres").lower()

    if DB_ENGINE == "sqlite":
        # Relative paths resolve against backend/ (this file's grandparent), not
        # the process cwd, so it works the same whether uvicorn/alembic/pytest is
        # launched from backend/ or the repo root.
        sqlite_path = Path(os.environ.get("SQLITE_PATH", "data/app.db"))
        if not sqlite_path.is_absolute():
            sqlite_path = Path(__file__).resolve().parent.parent.parent / sqlite_path
        sqlite_path.parent.mkdir(parents=True, exist_ok=True)
        DATABASE_URL = f"sqlite:///{sqlite_path}"
    elif DB_ENGINE == "postgres":
        DATABASE_URL = (
            f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}"
            f"@{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DB']}"
        )
    else:
        raise RuntimeError(f"Unknown DB_ENGINE={DB_ENGINE!r}; expected 'postgres' or 'sqlite'")

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
