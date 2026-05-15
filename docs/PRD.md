# FinRoute PRD

## 1. Product Definition

FinRoute is an advisor-facing AI financial portfolio planning system. It receives a customer's financial statement, goals, and risk profile, then produces a reviewable portfolio proposal draft that includes financial diagnosis, goal-based allocation, product category/product candidates, document-grounded explanations, and customer/advisor-facing reports.

The first product version is not a customer self-service app and does not complete product enrollment. It is an advisor support tool.

## 2. Users

| User | Goal | MVP Treatment |
|---|---|---|
| Advisor | Create diagnosis, allocation, recommendation, and proposal drafts quickly | P0 |
| Admin | Manage products, documents, users, and rule settings | P0/P1 depending on feature |
| Reviewer | Review portfolio outcomes and audit changes | P1 |
| Customer | Receive advisor-reviewed explanations and proposal documents | No direct MVP login |

Reviewer approval screens are not part of the first MVP. The first MVP includes advisor review and manual editing.

## 3. Product Principles

- Diagnose before recommending products.
- Use deterministic backend logic for metrics, rule checks, filtering, scoring, and allocation.
- Use RAG/LLM only for explanation, summarization, comparison copy, and proposal wording.
- Keep every generated plan and recommendation editable by an advisor.
- Store audit logs for generation, edits, exports, document uploads, and admin changes.
- Generate product explanations only from uploaded product documents.

## 4. MVP Preconditions

These are release gates for production-ready MVP implementation.

1. Legal and regulatory review is completed and documented.
2. Standard financial statement Excel template v1 is finalized.
3. Initial product DB input scope, owner, and reviewer are assigned.
4. Minimum RAG document set, owner, and freshness rules are assigned.

Do not treat advisor review as legal immunity. It is an operational control that must be paired with legal review and traceable records.

## 5. MVP Scope

### In Scope

- Advisor authentication baseline
- Customer CRUD
- Financial statement Excel upload and parsing
- Manual correction of parsed financial fields
- Financial metric calculation and diagnosis tags
- Goal and risk profile input
- Deterministic portfolio allocation
- Advisor manual override and rationale capture
- Product category mapping
- Product DB management
- Product hard filtering and weighted scoring
- Product document upload and retrieval
- RAG-generated recommendation rationale with source references
- Customer/advisor proposal preview
- PDF report generation
- Audit logging

### Out of Scope

- Direct customer self-service app
- Automatic product enrollment/subscription
- MyData or bank/insurance API aggregation
- Real-time market-based rebalancing
- Autonomous legal suitability approval
- Full compliance engine beyond MVP traceability, review gates, and disclaimers

## 6. Functional Requirements

| ID | Feature | Priority | Acceptance Criteria |
|---|---|---|---|
| FR-001 | Customer creation | P0 | Required fields create a customer assigned to an advisor |
| FR-002 | Excel upload | P0 | Standard template v1 parses into structured statement data |
| FR-003 | Missing value validation | P0 | Required missing fields block analysis and show actionable errors |
| FR-004 | Financial metrics | P0 | Metrics match documented formulas with explicit zero/missing handling |
| FR-005 | Diagnosis classification | P0 | One or more diagnosis tags are generated deterministically |
| FR-006 | Portfolio allocation | P0 | Monthly available funds are itemized by purpose with rationales |
| FR-007 | Product category mapping | P0 | Allocation items map to allowed product categories |
| FR-008 | Product candidate filtering | P0 | Ineligible products are excluded with reasons |
| FR-009 | RAG rationale generation | P0 | Product explanations include source refs or insufficient evidence |
| FR-010 | PDF proposal | P0 | Advisor can generate a downloadable report |
| FR-011 | Advisor manual edits | P1 | Allocation/product changes persist with rationale |
| FR-012 | Edit audit trail | P1 | Before/after payloads are recorded |
| FR-013 | Product comparison table | P1 | Two or more candidates can be compared with scoring details |
| FR-014 | Admin product DB | P1 | Products can be created, updated, suspended, or closed |
| FR-015 | Document version management | P1 | Product documents track version and validity windows |

## 7. Success Metrics

### User Workflow Targets

| Metric | Target |
|---|---:|
| Financial diagnosis draft generation workflow | within 5 minutes |
| Portfolio proposal draft workflow | within 1 minute after required inputs |
| Advisor-editable finalization rate | 95% or higher |
| Product rationale generation coverage | 90% or higher where documents exist |

### System Response Targets

| Operation | Target |
|---|---:|
| Excel parsing | within 5 seconds |
| Deterministic diagnosis calculation | within 3 seconds |
| Deterministic portfolio allocation | within 3 seconds |
| RAG rationale generation | within 15 seconds |
| PDF generation | within 30 seconds |

## 8. Main Workflow

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

## 9. Release Checklist

- Legal/regulatory MVP review is documented.
- Excel template v1 and parser validation rules are finalized.
- Customer registration through PDF export works end to end.
- At least five representative fixtures pass.
- Initial product DB scope is populated and reviewed.
- RAG explanations include source refs or insufficient evidence.
- Audit logs are written for generation, edit, export, admin, and document events.
- User-facing validation errors are actionable.

## 10. Open Decisions

- Exact legal interpretation of recommendation and investment-advice boundaries.
- Initial product category and product count for MVP demo/launch.
- Product data owner and reviewer.
- RAG document management owner and freshness process.
- Customer proposal visual design.
