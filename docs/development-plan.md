# Development Plan

## 1. Summary

This plan turns the current PRD and design documents into an implementation sequence. The first MVP is an advisor-facing workflow that creates a reviewable, explainable, customer-specific portfolio proposal from a standard financial statement Excel file.

The highest-risk prerequisites are legal/regulatory review and the standard financial statement template. They are Phase 0 decision gates.

Implementation status is tracked separately in `docs/implementation-status.md`.

## 2. Phase 0: Decision Gates

Do this before production-ready implementation of parser, recommendation, RAG, or report workflows.

| Gate | Output | Owner |
|---|---|---|
| Legal/regulatory review scope | Completed review memo or tracked approval record | TBD |
| Standard Excel template v1 | Finalized template spec and sample workbook | TBD |
| Initial product DB scope | Product count, categories, data owner, reviewer | TBD |
| Minimum RAG document set | Required document types and document owner | TBD |

Phase 0 acceptance criteria:

- `docs/compliance-review.md` has review status and owner filled in.
- `docs/financial-statement-template.md` matches the actual sample workbook.
- Initial product DB scope defines minimum product count for MVP demo/launch.
- Each MVP product has sale status, risk level, minimum payment, recommended term, purpose tags, and at least one document.

## 3. Phase 1: Foundation

Build the repository and runtime foundation.

Status: implemented.

- Scaffold monorepo: `apps/web`, `apps/api`, `infra/compose`.
- Add FastAPI app, health check, settings, test runner.
- Add Next.js app, base layout, route skeleton.
- Add PostgreSQL + pgvector Docker Compose.
- Add SQLAlchemy, Alembic, base models, migration workflow.
- Add `.env.example`.
- Keep documentation structure current.

Acceptance criteria:

- API health check works.
- Web app renders a basic advisor dashboard/workflow shell.
- Database migration command runs.
- Local environment can be started from documented commands.

## 4. Phase 2: Customer and Financial Statement

- Implement customer CRUD.
- Implement standard Excel v1 upload.
- Parse income, expense, asset, liability, and goal sheets.
- Validate missing columns, required values, numeric types, booleans, dates, and enums.
- Store original file through storage adapter.
- Build review/correction API and UI.
- Add five standard financial statement fixtures.

Status: customer CRUD vertical slice implemented. Financial statement storage, Excel parsing, review/correction UI, and fixtures remain pending.

Acceptance criteria:

- Standard workbook parses into normalized statement and line item tables.
- Invalid workbook returns actionable validation errors.
- Advisor can manually correct parsed values.
- Upload and correction write audit logs.

## 5. Phase 3: Diagnosis Engine

- Implement financial metrics:
  - monthly surplus
  - saving ratio
  - liquidity ratio
  - debt burden ratio
- Implement diagnosis tags:
  - `LIQUIDITY_SHORTAGE`
  - `DEBT_PRIORITY`
  - `GOAL_FUNDING_PRESSURE`
  - `RETIREMENT_PREPARATION_GAP`
  - `INVESTMENT_CAPACITY_AVAILABLE`
  - `PROTECTION_GAP` only when supporting data exists
- Persist structured issues and deterministic rationales.
- Build diagnosis API and UI table.

Acceptance criteria:

- Divide-by-zero and missing values are explicit.
- Multiple diagnosis tags can be stored.
- Diagnosis output separates metrics, tags, issues, and generated copy.

## 6. Phase 4: Portfolio Engine

- Implement goal horizon classification: `SHORT`, `MID`, `LONG`.
- Calculate monthly required amount per goal.
- Map diagnosis tags to allocation priority.
- Handle edge cases:
  - monthly available amount <= 0
  - emergency reserve shortage
  - high-cost debt
  - urgent goals exceeding available amount
  - multiple diagnosis tag conflicts
- Implement advisor manual overrides with reason capture.
- Write `PORTFOLIO_GENERATED` and `PORTFOLIO_MANUALLY_EDITED` audit events.

Acceptance criteria:

- Allocation items include term bucket, amount, goal link, and rationale.
- New investment is not recommended when monthly available amount is <= 0.
- Manual overrides preserve before/after values and advisor rationale.

## 7. Phase 5: Product Recommendation

- Implement product DB schema and admin CRUD.
- Add seed/import structure for initial products.
- Implement product category mapping.
- Implement hard filters:
  - sale status
  - risk compatibility
  - minimum monthly payment
  - recommended term
  - purpose fit
- Implement weighted scoring and sub-score persistence.
- Store exclusion reasons where feasible.
- Include protection/coverage mapping through `coverage_tags`.

Acceptance criteria:

- Hard filters always run before scoring.
- Filtered products cannot be revived by score.
- Recommendation output includes score, sub-scores, deterministic reason, and exclusion details.

## 8. Phase 6: RAG Layer

- Implement product document upload.
- Store document version, validity, sale status snapshot, source filename, and document type.
- Chunk documents and index with pgvector.
- Retrieve with product/document metadata filtering.
- Implement citation-required grounded generation.
- Implement insufficient evidence flag.
- Show UI warning badge and `문서 근거 부족` when evidence is insufficient.

Acceptance criteria:

- Product with no current supporting document returns insufficient evidence.
- Generated explanations include source refs.
- Outdated or sale-stopped documents are excluded from current evidence.
- Customer and advisor explanations are separate.

## 9. Phase 7: Reports

- Implement customer and advisor report preview.
- Implement PDF export.
- Include input summary, metrics, diagnosis, allocation, recommendations, cautions, source refs, and advisor edits.
- Persist `advisor_id`, `generated_by`, `review_status`, and file URL.
- Write `REPORT_EXPORTED` audit logs.

Acceptance criteria:

- Advisor can preview before export.
- Customer report avoids unsupported claims.
- Advisor report includes scoring details, source refs, and edit history.

## 10. Phase 8: Stabilization

- Add unit tests for calculations, diagnosis, allocation, hard filters, scoring, and RAG evidence handling.
- Add integration test for customer creation through report preview/export.
- Add frontend smoke tests for the main workflow.
- Run RAG quality fixture evaluation.
- Review validation messages and failure states.
- Update docs for implementation decisions.

Acceptance criteria:

- End-to-end vertical slice passes.
- Fixture set covers five representative customer types.
- Release checklist in `docs/PRD.md` is satisfied or gaps are documented.

## 11. Test Plan

### Compliance and Document Checks

- MVP preconditions appear in `docs/PRD.md` and this document.
- `AGENTS.md` has no broken external copied text.
- Reviewer role is marked P1, not first-MVP required.

### Parser Tests

- Standard Excel v1 parses successfully.
- Required sheet missing.
- Required column missing.
- Numeric type invalid.
- Date type invalid.
- Empty required value.
- Manual correction changes validation status.

### Portfolio Tests

- Liquidity shortage + debt pressure.
- Monthly available amount <= 0.
- Mid-term and long-term goal conflict.
- Advisor override stores before/after audit.

### Product Recommendation Tests

- Sale-stopped product excluded.
- Risk-incompatible product excluded.
- Minimum payment exceeds allocation.
- Term conflicts with goal horizon.
- Hard filter exclusion reasons and scoring sub-components persist.

### RAG Tests

- No product document returns insufficient evidence.
- Expired document excluded.
- Source refs missing causes rejection or regeneration.
- Customer/advisor copy separated.
- Caution summary is document-supported.

## 12. Assumptions

- Legal conclusions are made by legal/compliance reviewers, not by implementation docs.
- The first MVP is an advisor-facing internal support tool.
- Reviewer approval screens are P1.
- If product DB or RAG documents are unavailable, the system can stop at product category recommendation.
- Excel parser production scope is not final until template v1 is finalized.
