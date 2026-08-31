#!/bin/bash
set -e
root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Starting database (docker compose)..."
if ! docker compose -f "$root/docker-compose.yml" up -d; then
  echo ""
  echo "Could not start the database - is Docker running?"
  echo "Start Docker, wait for it to finish loading, then re-run this script."
  exit 1
fi

echo "Starting backend (FastAPI, dev/reload) in background..."
(cd "$root/backend" && uv run uvicorn app.main:app --reload) &
backend_pid=$!

echo "Starting frontend (Vite, dev) in background..."
(cd "$root/frontend" && bun run dev) &
frontend_pid=$!

echo ""
echo "All services starting."
echo "  - DB: http://localhost:5432"
echo "  - Backend: http://localhost:8000 (Swagger: http://localhost:8000/docs)"
echo "  - Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop all services."
echo ""

trap "kill $backend_pid $frontend_pid 2>/dev/null; exit" INT TERM
wait
