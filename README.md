# FastAPI + React Template

A minimal template for building modern web applications with FastAPI and React+TypeScript.

I didn't like the first two templates that I tried, so I said screw it and rolled my own. 

The goal of this template is to go from idea to MVP/POC as fast as possible. 

This will be my go-to when spinning up personal projects, so it may change over time, or I may abandon it completely.

I also tried to aim for a beginner-friendly setup. -Hence, the long ReadMe-

I remember how overwhelming it was wading through some bloated template in an attempt to set up some app I thought up. 

That sucks. 

So yeah, 
- no admin panel
- no SMTP integration
- no auth
- no (or less) cognitive overload while trying to sort through a bunch of code you don't want or need. 

**Why this template?**
- **Batteries included:** Database migrations, linting, testing, CI/CD out of the box
- **Modular backend:** Separate `api/` and `common/` layers for clean architecture
- **Modern tooling:** Vite + Bun on frontend, FastAPI + SQLAlchemy on backend
- **Type-safe:** TypeScript on frontend, Pydantic on backend

**Stack:**
- Backend: FastAPI + SQLAlchemy + Pydantic + PostgreSQL
- Frontend: React 19 + TypeScript + Vite + Bun + React Router
- Migrations: Alembic
- Linting: Ruff (Python) + Oxlint (TypeScript/React)
- Testing: pytest (backend) + vitest (frontend)
- CI/CD: GitHub Actions

## Quick Start

### Prerequisites
- Docker & Docker Compose (only needed for the Postgres setup - skip it if you leave the default `DB_ENGINE=sqlite`, see [Database](#database))
- `uv` (Python package manager) - [install](https://docs.astral.sh/uv/getting-started/installation/)
- `bun` (JavaScript runtime) - [install](https://bun.sh/get)

### Install Dependencies

**Backend:**
```bash
cd backend
uv sync
```

**Frontend:**
```bash
cd frontend
bun install
```

### Development

1. **Open the workspace** in VS Code:
   ```bash
   code todo_app.code-workspace
   ```
   Extensions will be recommended; accept them for Python/ruff and TypeScript/oxlint linting.

2. **Start the stack** (database, backend, frontend all in dev mode):
   ```bash
   # macOS / Linux
   ./start.sh

   # Windows PowerShell
   .\start.ps1
   ```

   This will:
   - Start Postgres via `docker compose up -d` (skipped if `.env` has `DB_ENGINE=sqlite`)
   - Launch FastAPI backend (with auto-reload) on `http://localhost:8000`
   - Launch Vite dev server on `http://localhost:5173`

3. **Stop services**:
   - Press Ctrl+C in the backend/frontend terminal windows
   - Stop database (Postgres mode only): `docker compose down` (from the root directory)

## Project Structure

```
backend/                    # FastAPI project (uv-managed)
├── app/
│   ├── main.py            # FastAPI app, middleware, router setup
│   ├── api/               # API routes and endpoint logic
│   │   ├── items.py       # Example: Item endpoints (GET, POST, etc.)
│   │   └── __init__.py
│   ├── common/            # Shared utilities, database, models, schemas
│   │   ├── database.py    # SQLAlchemy engine, Base, session, get_db()
│   │   ├── models.py      # ORM models (Item example)
│   │   ├── schemas.py     # Pydantic schemas (requests/responses)
│   │   ├── logging.py     # Logging configuration
│   │   └── __init__.py
│   └── __init__.py
├── tests/                 # Test suite (separate projects)
│   ├── conftest.py        # Shared fixtures, database setup
│   ├── test_api/          # Tests for API endpoints
│   │   ├── test_items.py  # Example: item endpoint tests
│   │   └── __init__.py
│   └── test_common/       # Tests for common utilities
│       ├── test_schemas.py # Example: schema/model tests
│       └── __init__.py
├── alembic/               # Database migrations
├── pyproject.toml         # Dependencies & config
└── .vscode/               # VS Code settings

frontend/                   # React+TypeScript app (bun + Vite + Tailwind)
├── src/
│   ├── components/        # Reusable components (Button, Input, Card)
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Card.tsx
│   │   └── index.ts
│   ├── pages/              # One file per route (see "Pages & Routing" below)
│   │   ├── Home.tsx        # /       - links to the other pages
│   │   ├── Health.tsx      # /health - backend connectivity check
│   │   └── Items.tsx       # /items  - list (GET) + create (POST) example
│   ├── main.tsx
│   ├── App.tsx             # Router shell: BrowserRouter + Routes
│   ├── App.test.tsx        # Example test: routing + the POST flow
│   ├── index.css          # Tailwind directives + global styles
│   └── ...
├── tailwind.config.ts     # Tailwind configuration
├── postcss.config.js      # PostCSS configuration
├── package.json
├── vitest.config.ts       # Test configuration
└── bun.lock

.env                        # Environment variables (gitignored)
.env.example               # Template
docker-compose.yml         # Postgres database service
todo_app.code-workspace   # VS Code multi-root workspace
.github/
  └── workflows/
      └── ci.yml           # GitHub Actions: lint + test on PR
.pre-commit-config.yaml    # Optional: Git hooks for code quality
```

### Backend Organization: `api/` vs `common/`

**`api/`** - Routes and endpoint logic
- New API endpoints (GET, POST, PUT, DELETE)
- Route-specific validation or business logic
- API error handling and responses
- Example: `app/api/items.py` contains all Item-related endpoints

**`common/`** - Shared utilities, data, and setup
- Database models (SQLAlchemy ORM)
- Pydantic schemas (request/response validation)
- Database engine, sessions, connection
- Logging, constants, helpers, decorators
- Any code used by multiple API modules
- Example: `app/common/models.py`, `app/common/schemas.py`

**File organization best practice:**
```
api/
  items.py      # All Item-related endpoints
  users.py      # All User-related endpoints
  auth.py       # Auth endpoints

common/
  models.py     # All SQLAlchemy models
  schemas.py    # All Pydantic schemas
  database.py   # Database setup
  logging.py    # Logging configuration
  utils.py      # Shared helpers
```

## Using This Template

### 1. Customize Project Name
Update in:
- `backend/pyproject.toml` (change `[project]` name)
- `frontend/package.json` (change `"name"`)
- `frontend/index.html` (change `<title>`)
- `README.md` (this file)
- `todo_app.code-workspace` (rename the file if desired)

### 2. Replace the Example (Item) Model
1. Delete `backend/app/api/items.py` and `backend/app/common/models.py`
2. Define your domain models in new `models.py`
3. Create Pydantic schemas in new `schemas.py`
4. Create route files in `api/` for each domain entity

### 3. Generate Database Migrations
```bash
cd backend
uv run alembic revision --autogenerate -m "Your migration description"
uv run alembic upgrade head
```

### 4. Write Tests
- API endpoint tests → `backend/tests/test_api/`
- Common utilities/schemas → `backend/tests/test_common/`

## Configuration

### Environment Variables
Create `.env` in the root (copy from `.env.example`):
```
DB_ENGINE=postgres        # or "sqlite"

# used when DB_ENGINE=postgres
POSTGRES_USER=todo
POSTGRES_PASSWORD=todo
POSTGRES_DB=todo
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# used when DB_ENGINE=sqlite
SQLITE_PATH=data/app.db
```

For production, use strong passwords and a managed database service (e.g., AWS RDS, Supabase).

An explicit `DATABASE_URL` env var always overrides `DB_ENGINE` (this is how tests and CI pin their own database without touching `.env` - see [Testing](#testing)).

## Backend Development

### Adding Dependencies
```bash
cd backend
uv add package_name          # Runtime dependency
uv add --dev package_name    # Development/testing only
uv sync                      # Install all dependencies
```

### Database Models
1. Define ORM models in `app/common/models.py`:
   ```python
   from sqlalchemy import Column, Integer, String
   from app.common.database import Base

   class Item(Base):
       __tablename__ = "items"
       id = Column(Integer, primary_key=True)
       name = Column(String, nullable=False)
   ```

   `app/common/__init__.py` imports `models` so every model gets registered on
   `Base.metadata` from one place. 
   
   This is what both `Base.metadata.create_all()`
   (used by tests) and `alembic revision --autogenerate` (used by migrations) rely
   on to see your tables. If you rename `models.py` or split it into multiple
   files, update that import.

2. Create Pydantic schemas in `app/common/schemas.py`:
   ```python
   from pydantic import BaseModel, ConfigDict

   class ItemCreate(BaseModel):
       name: str

   class Item(ItemCreate):
       id: int
       model_config = ConfigDict(from_attributes=True)
   ```

3. Add routes in `app/api/items.py`:
   ```python
   from fastapi import APIRouter, Depends
   from sqlalchemy.orm import Session
   from app.common.database import get_db
   from app.common import models, schemas

   router = APIRouter(prefix="/items", tags=["items"])

   @router.post("", response_model=schemas.Item)
   def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
       db_item = models.Item(**item.model_dump())
       db.add(db_item)
       db.commit()
       db.refresh(db_item)
       return db_item
   ```

4. Include router in `app/main.py`:
   ```python
   from app.api import items
   app.include_router(items.router)
   ```

5. Generate and run migration:
   ```bash
   uv run alembic revision --autogenerate -m "Add items table"
   uv run alembic upgrade head
   ```

### Testing

#### Run All Tests
```bash
cd backend
uv run pytest
```

#### Run API Tests Only
```bash
cd backend
uv run pytest tests/test_api/
```

#### Run Common Tests Only
```bash
cd backend
uv run pytest tests/test_common/
```

#### Run Specific Test File
```bash
cd backend
uv run pytest tests/test_api/test_items.py
```

#### Run with Verbose Output
```bash
cd backend
uv run pytest -v
```

**Test Database:** By default, tests run against an in-memory SQLite database, so
`uv run pytest` works with zero setup; no Docker, no `.env`. Each test function
automatically:
- Drops and recreates all tables
- Yields a fresh database session
- Cleans up after itself

Set `DATABASE_URL` yourself (e.g. to the docker-compose Postgres, or export the
same value CI uses) to run the suite against real Postgres instead. 
Probably worth doing before relying on any Postgres-specific behavior (types, functions, constraints)
that SQLite won't catch. CI always runs against real Postgres.

**Example test (api):**
```python
# tests/test_api/test_items.py
def test_create_item(client):
    response = client.post("/items", json={"name": "Learn Rust"})
    assert response.status_code == 200
    assert response.json()["name"] == "Learn Rust"
```

**Example test (common):**
```python
# tests/test_common/test_schemas.py
from app.common.models import Item
from app.common.schemas import Item as ItemSchema

def test_item_schema_from_orm():
    item = Item(id=1, name="Test")
    schema = ItemSchema.model_validate(item)
    assert schema.id == 1
    assert schema.name == "Test"
```

### Linting & Formatting
```bash
cd backend
uv run ruff check .        # Check for issues
uv run ruff check --fix .  # Auto-fix issues
```

Ruff is configured in `pyproject.toml` and runs automatically on save in VS Code.

### Logging

Basic logging is configured in `app/common/logging.py` and used throughout:

```python
from app.common.logging import logger

logger.info("User created")
logger.error("Database error", exc_info=True)
```

Logs appear in stdout with timestamps and log levels. For production, configure to write to files or a log aggregator (e.g., ELK, Datadog).

### Error Handling

A global exception handler in `app/main.py` catches unhandled exceptions and returns a safe error response:

```python
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
```

### Auto-Generated API Docs

FastAPI automatically generates interactive API documentation:

- **Swagger UI** - `http://localhost:8000/docs`
- **ReDoc** - `http://localhost:8000/redoc`

Both are interactive: test endpoints, see request/response schemas, and explore all routes. Docs are generated from route docstrings and type hints.

**Add docstrings to your routes:**

```python
@router.get("/{item_id}", response_model=ItemSchema)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Retrieve a single item by ID."""
    return db.query(Item).filter(Item.id == item_id).first()
```

**Example endpoints (from template):**
```
GET  /health          # Server status
GET  /items           # List all items
POST /items           # Create an item
GET  /items/{id}      # Get single item
```

## Frontend Development

### Pages & Routing

`App.tsx` is just a router shell - [React Router](https://reactrouter.com/) mapping
paths to page components:

```tsx
<BrowserRouter>
  <Routes>
    <Route path="/" element={<Home />} />
    <Route path="/health" element={<Health />} />
    <Route path="/items" element={<Items />} />
  </Routes>
</BrowserRouter>
```

Each route's page lives in `src/pages/`, one file per route. The three shipped pages
are deliberately tiny, and each demonstrates one thing so you can delete whichever
you don't need without untangling it from the others:
- **`Home.tsx`** - nothing but two `<Link>`s. Proves page separation / routing works.
- **`Health.tsx`** - pings the backend's `GET /health` and shows whether it's
  reachable. Proves the two halves of the stack are wired together (CORS, `fetch`).
- **`Items.tsx`** - lists items (`GET /items`) and a form to add one
  (`POST /items`). Proves a full request/response round-trip, including sending a
  JSON body.

Add a new page by dropping a file in `pages/` and a `<Route>` for it in `App.tsx`.

By default pages call `http://localhost:8000`; set `VITE_API_URL` in `frontend/.env`
to point elsewhere.

**Deploying:** these routes are client-side (React Router, not server-rendered), so a
direct load or refresh on `/health` or `/items` only works if your host serves
`index.html` for unmatched paths (Vite's dev server and `vite preview` already do
this). Most static hosts (Netlify, Vercel, S3+CloudFront, nginx) need this configured
explicitly as an SPA fallback / rewrite rule, or those routes will 404. ([Check out ReactRouter's SPA guide](https://reactrouter.com/how-to/spa))

### Styling with Tailwind CSS

This template uses **Tailwind CSS** for styling. Tailwind is a utility-first CSS framework. 

You compose styles using class names. - [docs](https://tailwindcss.com/docs/styling-with-utility-classes)

I included these compnents as exampled to show:
- Class Names can get crazy long.
- Creating a component keeps things DRY. 

Example:
```tsx
<button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
  Click me
</button>
```

See `tailwind.config.ts` to customize theme colors, typography, spacing, etc. Plain CSS in `src/index.css` layers on top and overrides Tailwind styles.

### Components

Reusable components live in `src/components/`. Each one wraps Tailwind utilities and accepts `className` to override styles:

```tsx
import { Button, Input, Card } from './components'

export function Page() {
  return (
    <Card className="max-w-md">
      <Input placeholder="Enter text" />
      <Button onClick={() => console.log('clicked')}>Submit</Button>
    </Card>
  )
}
```

Add more components as needed; the pattern is simple: compose Tailwind classes, accept `className` for overrides.

### Adding Dependencies
```bash
cd frontend
bun add package_name       # Runtime dependency
bun add -D package_name    # Dev dependency
```

### Building for Production
```bash
bun run build   # Create optimized build in dist/
```

### Testing

#### Run All Tests
```bash
cd frontend
bun run test           # Watch mode
bun run test --run     # Run once and exit (for CI)
```

#### Run Tests in Watch Mode
```bash
cd frontend
bun run test
```

Tests use `vitest` (Vite's test runner) and `@testing-library/react`.

**Example test:**
```typescript
// src/App.test.tsx - since App is just the router, tests render it and navigate
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from './App'

it('navigates from home to the health page', async () => {
  const user = userEvent.setup()
  render(<App />)

  await user.click(screen.getByRole('link', { name: 'Health Check' }))

  expect(screen.getByRole('heading', { name: 'Health Check' })).toBeDefined()
})
```

`App` renders its own `BrowserRouter`, which reads real browser history. If a test
navigates, reset the URL in `beforeEach` (`window.history.pushState({}, '', '/')`) so
later tests don't inherit it.

### Linting
```bash
bun run lint   # Oxlint checks (configured in .oxlintrc.json)
```

## Database

Two persistence layers, toggled by `DB_ENGINE` in `.env`:

- **`postgres`** - runs in Docker via `docker compose`. Connection details in `.env` (`POSTGRES_*`).
- **`sqlite`** (default) - a local file at `backend/<SQLITE_PATH>` (default `backend/data/app.db`). No Docker needed;
  `start.sh`/`start.ps1` skip `docker compose up` entirely when this is set. The file (and its parent dir)
  is created automatically on first run, persists between runs, and is gitignored (`backend/data/`) -
  it's a local dev convenience, not something to commit or share between machines.

Migrations (`alembic upgrade head`, etc.) work the same either way - they read the same computed
`DATABASE_URL`. Note SQLite has weaker `ALTER TABLE` support than Postgres, so a future
autogenerated migration that alters an existing column/constraint may need
[batch mode](https://alembic.sqlalchemy.org/en/latest/batch.html) to apply cleanly on SQLite.

Switching `DB_ENGINE` doesn't migrate data between backends - each keeps its own separate
database/file, so switching starts you on an empty schema until you run migrations again.

### Useful Commands
```bash
# --- Postgres ---
# View logs
docker compose logs db

# Connect directly with psql
psql postgresql://todo:todo@localhost:5432/todo

# Reset database (destroy all data)
docker compose down -v

# --- SQLite ---
# Inspect the file directly
sqlite3 backend/data/app.db

# Reset database (destroy all data)
rm backend/data/app.db
```

## Testing & CI/CD

### Running Tests Locally

**Backend:**
```bash
uv run pytest              # Run all backend tests
uv run pytest tests/test_api/       # API tests only
uv run pytest tests/test_common/    # Common tests only
uv run pytest -v           # Verbose output
```

**Frontend:**
```bash
bun run test --run    # Run once and exit (for CI)
bun run test          # Watch mode
```

Backend tests use in-memory SQLite by default (real Postgres in CI, or locally if you set `DATABASE_URL`); frontend uses `vitest` + `@testing-library/react`. See "Backend Development > Testing" above for detailed examples.

### GitHub Actions (CI)
- Triggered on: push to `main`, all PRs
- Runs:
  - `ruff check` (backend linting)
  - `oxlint` (frontend linting)
  - `pytest` (backend tests)
  - `vitest` (frontend tests)
- View results in PR checks or "Actions" tab

### Pre-commit Hooks (Optional)
Run linting & formatting before every commit:
```bash
pip install pre-commit
pre-commit install
```

Configuration in `.pre-commit-config.yaml`. To skip (not recommended):
```bash
git commit --no-verify
```

## Debugging

### Backend
- Uvicorn logs appear in the backend terminal; check for errors
- Add `print()` statements or use a debugger
- API responses visible in browser DevTools or via `curl`:
  ```bash
  curl -X GET http://localhost:8000/items
  ```
    - But I would set up something like [insomnia](https://insomnia.rest/)

### Frontend
- Vite dev server logs in the frontend terminal
- Browser DevTools (F12) for runtime debugging and network inspection
- React DevTools browser extension helps with component debugging


## What's Not Included

This template aims provides a solid foundation to build your stuff on, but deliberately omits features you'll want to add based on your specific needs:

- **Authentication & Authorization**
- **Environment-specific config** - Separate settings for dev, staging, production
- **Deployment containers** 
- **Secrets management** 
- **Feature flags**
- **Job queues** 
- **Caching layer**
- **Admin panel**

## Next Steps

1. Customize the app name and environment
2. Replace the Item example with your domain models
3. Design your database schema in `app/common/models.py`
4. Add API endpoints in `app/api/`
5. Build your frontend in `src/`
6. Write tests in `tests/test_api/` and `tests/test_common/`
7. Push to GitHub and watch CI run


