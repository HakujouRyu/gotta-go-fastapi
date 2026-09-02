# Starts the whole todo app stack for local development:
#   - Postgres via docker compose (skipped if .env has DB_ENGINE=sqlite)
#   - FastAPI backend (uv, --reload) in its own window
#   - React frontend (bun, --watch dev server) in its own window
$ErrorActionPreference = "Stop"
$root = $PSScriptRoot

# Read DB_ENGINE out of .env (defaults to postgres, same as backend/app/common/database.py).
$dbEngine = "postgres"
$envFile = Join-Path $root ".env"
if (Test-Path $envFile) {
    $line = Get-Content $envFile | Where-Object { $_ -match '^DB_ENGINE=' } | Select-Object -Last 1
    if ($line) { $dbEngine = ($line -split '=', 2)[1].Trim() }
}

if ($dbEngine -eq "sqlite") {
    Write-Host "DB_ENGINE=sqlite - skipping docker compose, backend will use its local SQLite file."
} else {
    Write-Host "Starting database (docker compose)..."
    docker compose -f "$root\docker-compose.yml" up -d
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "Could not start the database - is Docker Desktop running?" -ForegroundColor Yellow
        Write-Host "Start Docker Desktop, wait for it to finish loading, then re-run this script." -ForegroundColor Yellow
        exit 1
    }
}

Write-Host "Starting backend (FastAPI, dev/reload) in a new window..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\backend'; uv run uvicorn app.main:app --reload"

Write-Host "Starting frontend (Vite, dev) in a new window..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\frontend'; bun run dev"

Write-Host "All services starting. DB: $dbEngine, backend and frontend in separate windows."
