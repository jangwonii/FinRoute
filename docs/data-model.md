# Data Model

## 1. Modeling Principles

- Keep financial statement line items normalized.
- Keep deterministic scoring data separate from generated AI text.
- Use JSONB only for flexible snapshots, AI payloads, settings, and audit before/after payloads.
- Use Alembic migrations for every schema change.
- Preserve traceability from customer issue to goal, allocation, product candidate, document evidence, and report output.

## 2. Core Entity Relationships

```text
User
 └─< Customer
      ├─< FinancialStatement
      │    ├─< IncomeItem
      │    ├─< ExpenseItem
      │    ├─< AssetItem
      │    └─< LiabilityItem
      ├─< FinancialGoal
      ├─< RiskProfile
      ├─< DiagnosisResult
      ├─< PortfolioPlan
      │    └─< PortfolioAllocation
      └─< ProposalReport

Product
 ├─< ProductDocument
 ├─< ProductDocumentChunk
 └─< ProductRecommendation
```

## 3. Main Tables

### users

| Column | Type | Notes |
|---|---|---|
| user_id | UUID PK | |
| email | varchar unique | login identifier |
| password_hash | varchar | |
| name | varchar | |
| role | enum | `ADMIN`, `ADVISOR`, `REVIEWER` |
| created_at | datetime | |
| updated_at | datetime | |

### customers

| Column | Type | Notes |
|---|---|---|
| customer_id | UUID PK | |
| advisor_id | UUID FK users | owning advisor |
| name | varchar | |
| birth_year | int nullable | |
| gender | varchar nullable | |
| occupation | varchar nullable | |
| household_type | varchar nullable | |
| memo | text nullable | avoid sensitive raw notes where possible |
| created_at | datetime | |
| updated_at | datetime | |

### financial_statements

| Column | Type | Notes |
|---|---|---|
| statement_id | UUID PK | |
| customer_id | UUID FK customers | |
| statement_date | date | |
| monthly_income_total | numeric | |
| monthly_expense_total | numeric | |
| monthly_debt_payment | numeric | |
| monthly_saving_amount | numeric nullable | |
| liquid_assets | numeric nullable | |
| monthly_essential_expenses | numeric nullable | |
| monthly_surplus | numeric | calculated snapshot |
| source_type | enum | `EXCEL`, `MANUAL` |
| original_file_url | varchar nullable | storage adapter URL/key |
| parser_version | varchar nullable | Excel template/parser version |
| validation_status | enum | `VALID`, `NEEDS_CORRECTION`, `INVALID` |
| created_at | datetime | |
| updated_at | datetime | |

### income_items

| Column | Type | Notes |
|---|---|---|
| income_id | UUID PK | |
| statement_id | UUID FK financial_statements | |
| income_type | varchar | salary, business, other |
| amount | numeric | |
| stability_level | enum nullable | `HIGH`, `MEDIUM`, `LOW` |

### expense_items

| Column | Type | Notes |
|---|---|---|
| expense_id | UUID PK | |
| statement_id | UUID FK financial_statements | |
| expense_type | varchar | housing, food, transport, insurance, etc. |
| amount | numeric | |
| is_fixed | boolean | |
| is_essential | boolean | supports liquidity ratio |

### asset_items

| Column | Type | Notes |
|---|---|---|
| asset_id | UUID PK | |
| statement_id | UUID FK financial_statements | |
| asset_type | varchar | cash, deposit, stock, real_estate, pension |
| amount | numeric | |
| liquidity_level | enum | `HIGH`, `MEDIUM`, `LOW` |

### liability_items

| Column | Type | Notes |
|---|---|---|
| liability_id | UUID PK | |
| statement_id | UUID FK financial_statements | |
| liability_type | varchar | credit loan, mortgage, etc. |
| outstanding_amount | numeric | |
| interest_rate | numeric nullable | |
| monthly_payment | numeric | |
| maturity_date | date nullable | |
| is_high_cost | boolean | derived or manually set |

### financial_goals

| Column | Type | Notes |
|---|---|---|
| goal_id | UUID PK | |
| customer_id | UUID FK customers | |
| goal_type | varchar | housing, retirement, education, etc. |
| target_amount | numeric | |
| current_prepared_amount | numeric default 0 | |
| target_date | date | |
| priority | int | lower number means higher priority |
| monthly_required_amount | numeric | calculated snapshot |
| created_at | datetime | |

### risk_profiles

| Column | Type | Notes |
|---|---|---|
| risk_profile_id | UUID PK | |
| customer_id | UUID FK customers | |
| risk_type | enum | `STABLE`, `STABLE_NEUTRAL`, `NEUTRAL`, `GROWTH`, `AGGRESSIVE` |
| risk_score | int | |
| source | varchar nullable | questionnaire/manual |
| assessed_at | datetime | |

### diagnosis_results

| Column | Type | Notes |
|---|---|---|
| diagnosis_id | UUID PK | |
| customer_id | UUID FK customers | |
| statement_id | UUID FK financial_statements | |
| saving_ratio | numeric nullable | |
| liquidity_ratio | numeric nullable | |
| debt_burden_ratio | numeric nullable | |
| financial_health_score | int nullable | |
| diagnosis_tags | varchar[] | multiple tags allowed |
| main_issues_json | jsonb | structured issue/rationale list |
| generated_summary | text nullable | LLM/RAG copy, not deterministic logic |
| created_at | datetime | |

### portfolio_plans

| Column | Type | Notes |
|---|---|---|
| portfolio_id | UUID PK | |
| customer_id | UUID FK customers | |
| diagnosis_id | UUID FK diagnosis_results | |
| monthly_available_amount | numeric | |
| plan_status | enum | `DRAFT`, `REVIEWED`, `FINAL` |
| total_short_term_amount | numeric | |
| total_mid_term_amount | numeric | |
| total_long_term_amount | numeric | |
| created_by | UUID FK users | |
| updated_by | UUID FK users nullable | |
| created_at | datetime | |
| updated_at | datetime | |

### portfolio_allocations

| Column | Type | Notes |
|---|---|---|
| allocation_id | UUID PK | |
| portfolio_id | UUID FK portfolio_plans | |
| goal_id | UUID FK financial_goals nullable | |
| allocation_type | varchar | `EMERGENCY`, `DEBT`, `HOUSING`, `RETIREMENT`, etc. |
| term_bucket | enum | `SHORT`, `MID`, `LONG` |
| monthly_amount | numeric | |
| rationale | text | deterministic rationale |
| is_manual_override | boolean | |
| override_reason | text nullable | advisor rationale |

### products

| Column | Type | Notes |
|---|---|---|
| product_id | UUID PK | |
| product_name | varchar | |
| product_category | varchar | deposit, insurance, pension, fund, protection, etc. |
| purpose_fit | varchar[] | allowed purposes |
| coverage_tags | varchar[] nullable | protection/coverage categories for insurance-like products |
| recommended_term_min_months | int nullable | |
| recommended_term_max_months | int nullable | |
| liquidity_level | enum | `HIGH`, `MEDIUM`, `LOW` |
| risk_level | enum | `LOW`, `MEDIUM`, `HIGH` |
| tax_benefit | boolean | |
| min_monthly_payment | numeric nullable | |
| sale_status | enum | `ACTIVE`, `SUSPENDED`, `CLOSED` |
| last_updated_at | datetime | |

### product_documents

| Column | Type | Notes |
|---|---|---|
| document_id | UUID PK | |
| product_id | UUID FK products | |
| document_type | varchar | brochure, terms, guide, FAQ, caution |
| version | varchar | |
| valid_from | date | |
| valid_to | date nullable | |
| sale_status | enum | inherited snapshot for retrieval filtering |
| source_filename | varchar | original filename |
| file_url | varchar | storage adapter URL/key |
| uploaded_by | UUID FK users | |
| uploaded_at | datetime | |

### product_document_chunks

| Column | Type | Notes |
|---|---|---|
| chunk_id | UUID PK | |
| document_id | UUID FK product_documents | |
| product_id | UUID FK products | duplicated for metadata filtering |
| chunk_index | int | |
| content | text | |
| embedding | vector | pgvector |
| metadata_json | jsonb | includes document_type, version, validity, source_filename |
| created_at | datetime | |

### product_recommendations

| Column | Type | Notes |
|---|---|---|
| recommendation_id | UUID PK | |
| portfolio_id | UUID FK portfolio_plans | |
| allocation_id | UUID FK portfolio_allocations | |
| product_id | UUID FK products | |
| fit_score | numeric | |
| sub_scores_json | jsonb | purpose, term, risk, payment, liquidity, tax |
| hard_filter_passed | boolean | |
| exclusion_reasons_json | jsonb nullable | for excluded candidates if stored |
| recommendation_rank | int | |
| system_reason | text | deterministic reason |
| rag_reason_json | jsonb nullable | structured generated fields |
| caution_summary | text nullable | |
| source_document_refs_json | jsonb nullable | |
| insufficient_evidence_flag | boolean default false | |
| created_at | datetime | |

### proposal_reports

| Column | Type | Notes |
|---|---|---|
| report_id | UUID PK | |
| customer_id | UUID FK customers | |
| portfolio_id | UUID FK portfolio_plans | |
| advisor_id | UUID FK users | advisor responsible for report |
| generated_by | UUID FK users | actor who generated report |
| report_type | enum | `CUSTOMER`, `ADVISOR` |
| review_status | enum | `DRAFT`, `ADVISOR_REVIEWED`, `FINAL` |
| file_url | varchar nullable | generated PDF storage key |
| generated_at | datetime | |

### audit_logs

| Column | Type | Notes |
|---|---|---|
| log_id | UUID PK | |
| actor_id | UUID FK users | |
| event_type | varchar | e.g. `REPORT_EXPORTED` |
| target_type | varchar | |
| target_id | UUID | |
| before_json | jsonb nullable | |
| after_json | jsonb nullable | |
| created_at | datetime | |

## 4. Required Audit Events

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
