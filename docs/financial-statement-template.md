# Financial Statement Template

## 1. Purpose

This document defines the standard financial statement Excel template v1 that the MVP parser targets. The template must be finalized before production-ready parser work begins.

## 2. Workbook Requirements

- File type: `.xlsx`
- Template version: `FINROUTE_STATEMENT_V1`
- Amount unit: KRW monthly amount unless explicitly stated otherwise
- Empty required cells are validation errors
- Optional cells may be corrected manually in the review screen

## 3. Required Sheets

| Sheet | Purpose | Required |
|---|---|---|
| `Customer` | Basic customer context | Yes |
| `Income` | Monthly income line items | Yes |
| `Expenses` | Monthly expense line items | Yes |
| `Assets` | Current asset line items | Yes |
| `Liabilities` | Debt line items | Yes |
| `Goals` | Financial goals | Yes for portfolio generation |

## 4. Customer Sheet

| Column | Required | Type | Notes |
|---|---|---|---|
| name | Yes | text | customer display name |
| birth_year | No | integer | four-digit year |
| gender | No | text | optional |
| occupation | No | text | optional |
| household_type | No | text | optional |
| statement_date | Yes | date | base date for statement |

## 5. Income Sheet

| Column | Required | Type | Notes |
|---|---|---|---|
| income_type | Yes | text | salary, business, other |
| amount | Yes | number | monthly KRW |
| stability_level | No | enum | `HIGH`, `MEDIUM`, `LOW` |

## 6. Expenses Sheet

| Column | Required | Type | Notes |
|---|---|---|---|
| expense_type | Yes | text | housing, food, transport, insurance, etc. |
| amount | Yes | number | monthly KRW |
| is_fixed | Yes | boolean | true/false |
| is_essential | Yes | boolean | used for liquidity ratio |

## 7. Assets Sheet

| Column | Required | Type | Notes |
|---|---|---|---|
| asset_type | Yes | text | cash, deposit, stock, real_estate, pension |
| amount | Yes | number | current KRW value |
| liquidity_level | Yes | enum | `HIGH`, `MEDIUM`, `LOW` |

## 8. Liabilities Sheet

| Column | Required | Type | Notes |
|---|---|---|---|
| liability_type | Yes | text | credit loan, mortgage, card loan, etc. |
| outstanding_amount | Yes | number | current KRW balance |
| interest_rate | No | number | annual percent |
| monthly_payment | Yes | number | monthly KRW |
| maturity_date | No | date | optional |
| is_high_cost | No | boolean | parser may derive from rate threshold later |

## 9. Goals Sheet

| Column | Required | Type | Notes |
|---|---|---|---|
| goal_type | Yes | text | housing, retirement, education, marriage, etc. |
| target_amount | Yes | number | KRW |
| current_prepared_amount | No | number | defaults to 0 |
| target_date | Yes | date | goal date |
| priority | Yes | integer | lower number means higher priority |

## 10. Parser Validation Rules

- Required sheets must exist.
- Required columns must exist exactly as documented for v1.
- Required cells must not be blank.
- Amount fields must be numeric and non-negative.
- Boolean fields must parse from `true/false`, `TRUE/FALSE`, `Y/N`, or documented localized aliases if added later.
- Date fields must parse to valid dates.
- Enum values must match allowed values.
- `statement_date` must be present before diagnosis.
- Goals are required before portfolio generation, but not before statement parsing.

## 11. Missing Value Handling

| Case | Behavior |
|---|---|
| Required structural element missing | Reject upload and show validation error |
| Required row value missing | Mark statement `NEEDS_CORRECTION` |
| Optional value missing | Allow upload and show correction prompt |
| Invalid numeric/date type | Mark affected row and block dependent calculations |

## 12. Fixture Set

Create five fixture workbooks once implementation starts:

1. liquidity shortage + debt pressure
2. mid-term housing goal + neutral risk
3. retirement-focused long-term planner
4. high surplus but weak goal structure
5. low income stability with limited allocation capacity

Fixture workbooks should live under `apps/api/tests/fixtures/financial_statements/` once the backend is scaffolded.
