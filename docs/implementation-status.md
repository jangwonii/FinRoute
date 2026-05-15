# Implementation Status

Last updated: 2026-05-15

This document summarizes what has been implemented so far, how to run it locally, and what remains before the next development phase.

## 1. Repository and Git

- Local Git repository initialized on branch `main`.
- Remote configured as `https://github.com/jangwonii/FinRoute.git`.
- Initial implementation pushed to `origin/main`.
- Initial commit:

```text
fafd13e feat: FinRoute 초기 개발 기반 구축
```

## 2. Implemented Scope

### Phase 1 Foundation

Implemented:

- Monorepo structure:
  - `apps/api`
  - `apps/web`
  - `infra/compose`
- FastAPI backend scaffold.
- Next.js App Router frontend scaffold.
- PostgreSQL + pgvector Docker Compose setup.
- Alembic migration workflow.
- Environment example file.
- API response envelope:

```json
{
  "data": {},
  "meta": {},
  "errors": []
}
```

### Customer CRUD Vertical Slice

Implemented as the first Phase 2 slice:

- SQLAlchemy models:
  - `User`
  - `Customer`
  - `AuditLog`
- Alembic migration:
  - `20260515_0001_foundation_customers.py`
- API endpoints:
  - `GET /health`
  - `GET /customers`
  - `POST /customers`
  - `GET /customers/{customer_id}`
  - `PATCH /customers/{customer_id}`
- Pagination metadata for customer list responses.
- Pydantic request and response schemas.
- Repository/service separation for customer persistence and workflow logic.
- Customer creation audit event:

```text
CUSTOMER_CREATED
```

Current auth assumption:

- A fixed development advisor is used until real `/auth` and RBAC are implemented.
- Development advisor ID:

```text
00000000-0000-0000-0000-000000000001
```

### Frontend

Implemented:

- Advisor workflow landing screen.
- Customer list loaded from the API.
- Customer creation form.
- API status check through `GET /health`.
- API client module at `apps/web/src/lib/api.ts`.

The current first screen is operational, not a marketing page.

## 3. Runtime Status

Local runtime confirmed:

- Web:

```text
http://127.0.0.1:3000
```

- API:

```text
http://127.0.0.1:8000/health
```

- PostgreSQL/pgvector container:

```text
finroute-postgres
```

The Docker container was started through Docker Desktop and reported healthy.

## 4. Local Development Commands

### Start Database

From the repository root:

```powershell
docker compose --env-file .env.example -f infra\compose\docker-compose.yml up -d
```

### Apply Migrations

```powershell
cd apps\api
alembic upgrade head
```

### Start API

```powershell
cd apps\api
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Start Web

PowerShell may block `npm.ps1`, so use `npm.cmd`.

```powershell
npm.cmd --prefix apps\web run dev -- --hostname 127.0.0.1 --port 3000
```

## 5. Verification Completed

Backend:

```powershell
cd apps\api
python -m pytest
ruff check .
alembic current
```

Latest known results:

- `python -m pytest`: 7 tests passed.
- `ruff check .`: passed.
- `alembic current`: `20260515_0001 (head)`.

Frontend:

```powershell
npm.cmd --prefix apps\web run build
```

Latest known result:

- Next.js production build passed.

Manual verification:

- `GET /health` returned `status=ok`.
- `GET /customers` returned a valid envelope and pagination metadata.
- Web root returned `200 OK`.
- Next.js `.next` cache corruption was fixed by stopping the dev server, deleting `.next`, and restarting the server.

## 6. Current Limitations

- Real authentication is not implemented yet.
- RBAC and advisor ownership are represented only by a fixed development advisor.
- Customer update does not yet write an audit event.
- Financial statement upload, Excel parsing, metrics, diagnosis, allocation, product recommendation, RAG, and reports are not implemented yet.
- Phase 0 release gates remain open:
  - legal/regulatory review owner and result
  - finalized standard Excel template v1 sample workbook
  - initial product DB owner/reviewer/scope
  - minimum RAG document set and document owner

Production-ready parser, recommendation, RAG, and report export work remains blocked until those release gates are resolved.

## 7. Recommended Next Development Step

Recommended next slice:

```text
FinancialStatement manual data model and API foundation
```

Suggested contents:

- Add `FinancialStatement`, `IncomeItem`, `ExpenseItem`, `AssetItem`, and `LiabilityItem` models.
- Add Alembic migration for normalized statement tables.
- Add manual create/read/update API before Excel parsing.
- Add deterministic metric calculation utilities with unit tests.
- Keep Excel upload as a later parser-specific layer after the template/sample workbook is final.

Reason:

- It continues Phase 2 without depending on the final Excel workbook.
- It gives the diagnosis engine stable structured inputs.
- It keeps deterministic financial logic testable before introducing file parsing complexity.
