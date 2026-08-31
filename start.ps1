# Starts the whole todo app stack for local development:
#   - Postgres via docker compose
#   - FastAPI backend (uv, --reload) in its own window
#   - React frontend (bun, --watch dev server) in its own window
$ErrorActionPreference = "Stop"
$root = $PSScriptRoot

Write-Host "Starting database (docker compose)..."
docker compose -f "$root\docker-compose.yml" up -d
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Could not start the database - is Docker Desktop running?" -ForegroundColor Yellow
    Write-Host "Start Docker Desktop, wait for it to finish loading, then re-run this script." -ForegroundColor Yellow
    exit 1
}

Write-Host "Starting backend (FastAPI, dev/reload) in a new window..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\backend'; uv run uvicorn app.main:app --reload"

Write-Host "Starting frontend (Vite, dev) in a new window..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\frontend'; bun run dev"

Write-Host "All services starting. DB via docker compose, backend and frontend in separate windows."
