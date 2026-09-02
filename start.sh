#!/bin/bash
set -e
root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Read DB_ENGINE out of .env (defaults to postgres, same as backend/app/common/database.py).
db_engine="$(grep -E '^DB_ENGINE=' "$root/.env" 2>/dev/null | tail -n1 | cut -d= -f2- | tr -d '[:space:]')"
db_engine="${db_engine:-postgres}"

if [ "$db_engine" = "sqlite" ]; then
  echo "DB_ENGINE=sqlite - skipping docker compose, backend will use its local SQLite file."
else
  echo "Starting database (docker compose)..."
  if ! docker compose -f "$root/docker-compose.yml" up -d; then
    echo ""
    echo "Could not start the database - is Docker running?"
    echo "Start Docker, wait for it to finish loading, then re-run this script."
    exit 1
  fi
fi

echo "Starting backend (FastAPI, dev/reload) in background..."
(cd "$root/backend" && uv run uvicorn app.main:app --reload) &
backend_pid=$!

echo "Starting frontend (Vite, dev) in background..."
(cd "$root/frontend" && bun run dev) &
frontend_pid=$!

echo ""
echo "All services starting."
if [ "$db_engine" != "sqlite" ]; then
  echo "  - DB: http://localhost:5432"
fi
echo "  - Backend: http://localhost:8000 (Swagger: http://localhost:8000/docs)"
echo "  - Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop all services."
echo ""

trap "kill $backend_pid $frontend_pid 2>/dev/null; exit" INT TERM
wait
