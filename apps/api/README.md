# FinRoute API

FastAPI backend for the FinRoute advisor workflow.

## Local Commands

```powershell
cd apps/api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m uvicorn app.main:app --reload
```

Health check:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Tests:

```powershell
python -m pytest
```

Migrations:

```powershell
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```
