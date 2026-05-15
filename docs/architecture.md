# Architecture

## 1. Overview

FinRoute uses a monorepo layout with a Next.js frontend and FastAPI backend. Deterministic financial logic stays in backend services. RAG and LLM features generate explanations only after deterministic diagnosis, allocation, filtering, and scoring are complete.

```text
[Web: Next.js]
        ↓
[API: FastAPI]
        ↓
[Domain Services]
  ├─ Customer Service
  ├─ Financial Statement Parser
  ├─ Financial Analysis Service
  ├─ Portfolio Engine
  ├─ Product Recommendation Engine
  ├─ RAG Service
  ├─ Report Service
  └─ Audit Service
        ↓
[Storage]
  ├─ PostgreSQL + pgvector
  ├─ Object/File Storage Adapter
  └─ Generated Report Storage
```

## 2. Repository Layout

```text
.
├─ AGENTS.md
├─ README.md
├─ docs/
├─ apps/
│  ├─ web/
│  │  ├─ src/
│  │  ├─ public/
│  │  └─ package.json
│  └─ api/
│     ├─ app/
│     │  ├─ api/
│     │  ├─ core/
│     │  ├─ db/
│     │  ├─ models/
│     │  ├─ schemas/
│     │  ├─ services/
│     │  ├─ repositories/
│     │  ├─ prompts/
│     │  └─ main.py
│     ├─ tests/
│     ├─ alembic/
│     └─ pyproject.toml
├─ packages/
│  └─ shared-types/
└─ infra/
   ├─ docker/
   └─ compose/
```

`packages/shared-types` is optional and should only be introduced if frontend/backend type sharing becomes valuable.

## 3. Backend Boundaries

| Layer | Responsibility |
|---|---|
| API routes | HTTP validation, authentication, response shaping |
| Schemas | Pydantic request/response contracts |
| Services | Domain workflows and transaction boundaries |
| Engines | Pure calculation, diagnosis, allocation, filtering, and scoring logic |
| Repositories | SQLAlchemy persistence and query composition |
| Prompts | Versioned prompt templates and structured output definitions |

Domain logic must not live in route handlers.

## 4. Frontend Boundaries

| Area | Responsibility |
|---|---|
| App routes | Workflow pages and route-level layout |
| Components | Reusable UI and table/form components |
| Forms | React Hook Form + Zod schemas close to each form |
| API hooks | TanStack Query hooks separated from pure UI |
| Workflow state | Step progress, draft states, and validation status |

The first screen should be the advisor workflow/dashboard, not a marketing page.

## 5. Storage

- PostgreSQL stores relational domain data.
- pgvector stores product document chunk embeddings.
- Uploaded files and generated PDFs must use a storage adapter.
- Local filesystem storage is allowed for development through the same abstraction.
- Do not hard-code permanent local paths in domain logic.

## 6. Security

- Use environment variables for secrets.
- Apply server-side authorization checks.
- Treat customer financial information as sensitive business data.
- Avoid logging raw personally sensitive data.
- Store audit logs for generation, edit, export, admin, and document events.

## 7. Release Gates

Production-ready parser, recommendation, RAG, and report workflows require:

1. documented compliance review scope and outcome
2. finalized Excel template v1
3. initial product DB scope and ownership
4. minimum RAG document set and ownership
