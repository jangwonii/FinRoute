# AGENTS.md

## 1. Purpose

This file is the implementation guide for Codex and other AI coding agents working in this repository. It defines the project principles, implementation boundaries, required documentation discipline, and sequencing rules that agents must follow when making code or documentation changes.

For product background and developer onboarding, use `README.md` and the documents under `docs/`.

---

## 2. Project Overview

FinRoute is an AI-assisted financial portfolio planning system for financial advisors. The system receives a customer's financial statement and goal information, analyzes the customer's financial condition, generates short-, mid-, and long-term allocation plans, maps suitable product categories and product candidates, retrieves supporting product documents with RAG, and creates advisor/customer-facing proposal reports.

The product is not a fully autonomous direct-to-consumer investment recommendation engine. It is an advisor support system. Final outputs must remain reviewable and editable by a human advisor.

---

## 3. Product Principles

Follow these principles in every implementation decision.

1. **Diagnosis before product recommendation**
   - Analyze the customer's condition first.
   - Identify core financial issues.
   - Generate allocation logic.
   - Only then map product categories and products.

2. **Use structured logic for decisions, use LLM/RAG for explanation**
   - Financial metrics, rule checks, filtering, and scoring must be deterministic backend logic.
   - RAG/LLM should generate explanations, summaries, comparison copy, and proposal wording.
   - Do not let the LLM decide numeric portfolio allocation by itself.

3. **Advisor-in-the-loop**
   - Every portfolio plan and product recommendation must be editable.
   - Store manual modifications and rationale when possible.
   - Treat advisor review as an operational control, not as legal immunity.

4. **Explainability**
   - Recommendation results must expose the reasoning chain:
     - customer issue
     - goal
     - portfolio allocation
     - matching product category
     - filtered product candidate
     - document-backed explanation

5. **Traceability**
   - Save audit logs for recommendation generation, user edits, report exports, and admin changes.

6. **Document-grounded RAG**
   - RAG must answer from uploaded product documents only.
   - If evidence is insufficient, return an explicit insufficient-evidence response rather than inventing details.

---

## 4. MVP Decision Gates

Do not implement the parser, product recommendation, RAG generation, or report export as production-ready features until these decision gates are documented.

1. Legal and regulatory review scope is defined and MVP release requirements are recorded.
2. Standard financial statement Excel template v1 is finalized.
3. Initial product DB scope, data owner, and reviewer are assigned.
4. Minimum RAG document set and document owner are assigned.

See:

- `docs/compliance-review.md`
- `docs/financial-statement-template.md`
- `docs/development-plan.md`

---

## 5. Recommended Tech Stack

### Frontend
- Next.js
- TypeScript
- App Router preferred
- Tailwind CSS
- React Hook Form + Zod for forms and validation
- TanStack Query for API state

### Backend
- Python 3.11+
- FastAPI
- Pydantic v2
- SQLAlchemy 2.x
- Alembic migrations
- PostgreSQL

### AI / RAG
- Vector store: pgvector by default unless a documented decision changes it
- RAG pipeline must support chunking, metadata filtering, retrieval, citation-required grounded generation, and insufficient evidence handling
- Prompt templates must be versioned in code or a dedicated configuration area

### File and Report Handling
- Excel parsing: pandas / openpyxl
- PDF generation: HTML-to-PDF, WeasyPrint, ReportLab, or another documented stack
- Store generated reports and uploaded source files through a storage abstraction, not hard-coded local paths

---

## 6. Repository Structure

Use this monorepo structure unless an explicit architecture decision changes it.

```text
.
├─ AGENTS.md
├─ README.md
├─ docs/
│  ├─ PRD.md
│  ├─ architecture.md
│  ├─ data-model.md
│  ├─ api-spec.md
│  ├─ ai-recommendation-logic.md
│  ├─ compliance-review.md
│  ├─ financial-statement-template.md
│  ├─ rag-quality.md
│  └─ development-plan.md
├─ apps/
│  ├─ web/
│  └─ api/
├─ packages/
│  └─ shared-types/
└─ infra/
   ├─ docker/
   └─ compose/
```

Preserve established conventions once implementation begins.

---

## 7. Core Domain Model

The implementation should revolve around these entities.

```text
User
Customer
FinancialStatement
IncomeItem
ExpenseItem
AssetItem
LiabilityItem
FinancialGoal
RiskProfile
DiagnosisResult
PortfolioPlan
PortfolioAllocation
Product
ProductDocument
ProductRecommendation
ProposalReport
AuditLog
```

Keep relations explicit. Use JSONB only for flexible analysis snapshots, AI output payloads, settings, and audit before/after payloads where relational modeling is not justified.

---

## 8. Required Business Logic

### Financial Metrics

Implement deterministic calculations.

```text
monthly_surplus = monthly_income_total - monthly_expense_total - monthly_debt_payment
saving_ratio = monthly_saving_amount / monthly_income_total
liquidity_ratio = liquid_assets / monthly_essential_expenses
debt_burden_ratio = monthly_debt_payment / monthly_income_total
```

Handle divide-by-zero and missing-value cases explicitly.

### Financial Diagnosis

At minimum, detect:

- `LIQUIDITY_SHORTAGE`
- `DEBT_PRIORITY`
- `GOAL_FUNDING_PRESSURE`
- `RETIREMENT_PREPARATION_GAP`
- `INVESTMENT_CAPACITY_AVAILABLE`

A customer may have multiple diagnosis tags.

### Portfolio Allocation

The allocation engine must allocate available monthly funds using deterministic rules.

Priority order:

1. Emergency liquidity reserve
2. High-cost debt repayment
3. Urgent short/mid-term goals
4. Minimum long-term preparation
5. Additional investment or savings optimization

The engine must expose rationales per allocation item and allow advisor overrides with stored rationale.

### Product Matching

Hard filters always run before scoring. Exclude products when:

- `sale_status` is not `ACTIVE`
- risk level is clearly incompatible with customer risk profile
- minimum monthly payment exceeds the allocated monthly amount
- recommended term is structurally inconsistent with the goal horizon
- product is not mapped to the relevant purpose

Use explainable weighted scoring after filters:

```text
purpose_fit: 30
term_fit: 20
risk_fit: 20
payment_fit: 15
liquidity_fit: 10
tax_benefit_fit: 5
```

Persist the final score, sub-scores, and exclusion reasons whenever feasible.

---

## 9. RAG Rules

Every chunk must preserve or inherit:

```text
product_id
document_id
document_type
version
valid_from
valid_to
sale_status
source_filename
chunk_index
```

Retrieval must use metadata filtering before or alongside semantic retrieval. Prefer active documents and newest valid versions. Do not mix outdated and current versions without clearly separating them.

The LLM output must be separated into:

```text
customer_friendly_reason
advisor_reason
caution_summary
source_document_refs
insufficient_evidence_flag
```

Do not hide uncertainty. UI must show a warning state when evidence is insufficient.

---

## 10. API Guidelines

Use REST endpoints with clear noun-based resources.

```text
/auth
/customers
/financial-statements
/goals
/risk-profiles
/diagnoses
/portfolio-plans
/products
/product-documents
/recommendations
/reports
/admin
```

Rules:

- Validate all request bodies with Pydantic.
- Use consistent response envelopes from the beginning.
- Return actionable validation errors.
- Paginate list endpoints.
- Keep generated AI content and deterministic scoring data separate.

---

## 11. Testing Requirements

Write focused tests for:

- financial metric calculations
- diagnosis classification rules
- portfolio allocation outcomes and edge cases
- product hard-filter logic
- product scoring logic
- document metadata handling
- insufficient evidence behavior
- report generation inputs

Create fixture datasets for:

1. liquidity shortage + debt pressure
2. mid-term housing goal + neutral risk
3. retirement-focused long-term planner
4. high surplus but weak goal structure
5. low income stability with limited allocation capacity

---

## 12. Security, Privacy, and Audit

Handle customer financial data as sensitive business data.

Implement or prepare for:

- RBAC
- server-side authorization checks
- audit logs
- careful handling of uploaded files
- no secrets in source code
- environment variables for credentials
- controlled exposure of generated reports

Audit at least:

```text
CUSTOMER_CREATED
STATEMENT_UPLOADED
DIAGNOSIS_GENERATED
PORTFOLIO_GENERATED
PORTFOLIO_MANUALLY_EDITED
PRODUCT_RECOMMENDATION_GENERATED
REPORT_EXPORTED
ADMIN_PRODUCT_UPDATED
DOCUMENT_UPLOADED
```

Do not log raw personally sensitive data unnecessarily.

---

## 13. Coding Standards

- Prefer explicit, readable code over clever abstractions.
- Keep domain logic out of controllers/routes.
- Use service/repository separation.
- Avoid duplication in financial rule logic.
- Introduce configuration constants for score thresholds and weights.
- Use type hints in Python.
- Use Pydantic schemas for I/O.
- Use SQLAlchemy models cleanly.
- Keep calculation utilities pure where possible.
- Use strict typing in TypeScript.
- Keep form schemas close to corresponding form modules.
- Keep API hooks separated from pure UI components.

---

## 14. Database and Migration Rules

- Use migrations for every schema change.
- Never rely on ad hoc table creation.
- Prefer normalized tables for financial statement line items.
- Use JSONB only for flexible snapshots, AI output payloads, settings, or audit before/after payloads.

---

## 15. Definition of Done

A task is done only when:

1. code is implemented
2. type and lint errors are addressed
3. tests are added or updated when appropriate
4. relevant docs are updated
5. the feature has a clear manual verification path
6. generated outputs are traceable to input data and business logic

---

## 16. Do Not Do These

Do not:

- invent product facts not present in structured DB or retrieved documents
- hardcode demo-only thresholds in deeply buried files
- mix deterministic calculation and LLM-generated judgment in one opaque function
- skip migrations for DB changes
- store unbounded raw AI prompts/results without structure
- build one massive service file that mixes parsing, diagnosis, portfolio, recommendation, and reporting
- treat advisor review as automatic legal immunity

---

## 17. Agent Work Rules

When given a development task:

1. inspect the repository first
2. identify which phase and module the task belongs to
3. summarize intended code changes before implementation if the task is large
4. implement the smallest coherent slice
5. run tests or provide the exact verification command
6. summarize changed files and remaining gaps

For large multi-step features, prefer incremental implementation over broad unverified changes.
