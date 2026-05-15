# FinRoute

FinRoute is an advisor-facing AI financial portfolio planning system. It helps a financial advisor analyze a customer's financial statement, diagnose financial issues, create a goal-based allocation plan, map suitable product categories and product candidates, retrieve product-document evidence with RAG, and generate reviewable proposal reports.

The product is an advisor support system, not a fully autonomous direct-to-consumer investment recommendation service.

## Current Status

This repository is in the documentation and planning stage. The original planning sources are preserved at the repository root:

- `ai_개인별_재무포트폴리오_서비스_기획_설계서.md`
- `Ai 재무포트폴리오 서비스 Prd.docx`

Implementation-facing documents are under `docs/`.

## Key Documents

- `docs/PRD.md`: product requirements and MVP scope
- `docs/architecture.md`: system architecture and repository layout
- `docs/data-model.md`: core entities and table design
- `docs/api-spec.md`: REST API groups and response rules
- `docs/ai-recommendation-logic.md`: deterministic diagnosis, allocation, and scoring logic
- `docs/compliance-review.md`: legal/regulatory review checklist and release gate
- `docs/financial-statement-template.md`: standard Excel template v1 specification
- `docs/rag-quality.md`: grounded generation and RAG quality rules
- `docs/development-plan.md`: phased implementation plan and acceptance gates

## MVP Direction

The first MVP focuses on an advisor workflow:

```text
Customer Select/Create
→ Upload Financial Statement
→ Review Parsed Data
→ Input Goals and Risk Profile
→ View Diagnosis
→ Review Portfolio Allocation
→ Review Product Recommendations
→ Review RAG Explanations
→ Generate Proposal Report
```

## Release Gates

The following must be documented before production-ready implementation of parser, recommendation, RAG, and report workflows:

1. Legal and regulatory review scope
2. Standard financial statement Excel template v1
3. Initial product DB scope and ownership
4. Minimum RAG document set and ownership

## Default Stack

- Frontend: Next.js, TypeScript, Tailwind CSS
- Backend: FastAPI, Python 3.11+, Pydantic v2, SQLAlchemy 2.x
- Database: PostgreSQL with pgvector
- Migrations: Alembic
- Excel parsing: pandas / openpyxl
- PDF generation: HTML-to-PDF or WeasyPrint

## Phase 1 Local Development

This repository now contains the Phase 1 foundation scaffold:

```text
apps/api      FastAPI backend
apps/web      Next.js advisor workflow shell
infra/compose PostgreSQL + pgvector Docker Compose
```

Create a local environment file before running services:

```powershell
Copy-Item .env.example .env
```

PowerShell may block `npm.ps1` on some Windows systems. Use `npm.cmd` for frontend
commands unless your execution policy is configured differently.

### Database

```powershell
docker compose --env-file ..\..\.env -f infra\compose\docker-compose.yml up -d
```

### API

```powershell
cd apps\api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m uvicorn app.main:app --reload
```

Verify:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
python -m pytest
alembic current
```

### Web

```powershell
cd apps\web
npm.cmd install
npm.cmd run dev
```

Open `http://localhost:3000` to view the advisor workflow shell.

Build check:

```powershell
npm.cmd run build
```
