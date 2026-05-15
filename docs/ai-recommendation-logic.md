# AI Recommendation Logic

## 1. Boundary

The system uses deterministic backend logic for financial calculations, diagnosis tags, allocation, product hard filters, and weighted scoring. LLM/RAG is used only for explanation, summary, comparison copy, and report wording after deterministic decisions are made.

## 2. Pipeline

```text
[1] Customer financial statement input
        ↓
[2] Data validation and metric calculation
        ↓
[3] Diagnosis tags and issue classification
        ↓
[4] Goal funding need calculation
        ↓
[5] Priority-based monthly allocation
        ↓
[6] Product category mapping
        ↓
[7] Product DB hard filtering and scoring
        ↓
[8] RAG-based rationale/caution generation
        ↓
[9] Proposal report generation
```

## 3. Financial Metrics

```text
monthly_surplus = monthly_income_total - monthly_expense_total - monthly_debt_payment
saving_ratio = monthly_saving_amount / monthly_income_total
liquidity_ratio = liquid_assets / monthly_essential_expenses
debt_burden_ratio = monthly_debt_payment / monthly_income_total
```

Rules:

- Division by zero returns an explicit unavailable metric state, not `0`.
- Missing required values block diagnosis.
- Missing optional values should be surfaced as lower-confidence or incomplete analysis where appropriate.

## 4. Diagnosis Tags

| Tag | Trigger Direction | Notes |
|---|---|---|
| `LIQUIDITY_SHORTAGE` | liquidity ratio below threshold | Emergency reserve priority |
| `DEBT_PRIORITY` | debt burden high or high-cost debt exists | Debt repayment priority |
| `GOAL_FUNDING_PRESSURE` | short/mid-term goals exceed feasible monthly funding | Goal tradeoff needed |
| `RETIREMENT_PREPARATION_GAP` | long-term preparation below minimum target | Minimum long-term allocation |
| `INVESTMENT_CAPACITY_AVAILABLE` | surplus remains after reserve/debt/urgent goals | Additional optimization |
| `PROTECTION_GAP` | insurance/protection data indicates gap | Requires supporting data |

A customer may have multiple tags.

## 5. Allocation Priority

Base priority:

1. Emergency liquidity reserve
2. High-cost debt repayment
3. Urgent short/mid-term goals
4. Minimum long-term preparation
5. Additional investment or savings optimization

## 6. Diagnosis-to-Allocation Mapping

| Diagnosis Tag | Allocation Effect | Rationale |
|---|---|---|
| `LIQUIDITY_SHORTAGE` | Increase `EMERGENCY` allocation before investment categories | Customer lacks near-term buffer |
| `DEBT_PRIORITY` | Allocate to `DEBT` after minimum liquidity floor | High-cost debt weakens cash flow |
| `GOAL_FUNDING_PRESSURE` | Prioritize urgent goals by date and declared priority | Goal deadlines create funding pressure |
| `RETIREMENT_PREPARATION_GAP` | Preserve minimum `RETIREMENT` allocation when feasible | Avoid fully deferring long-term preparation |
| `INVESTMENT_CAPACITY_AVAILABLE` | Allocate surplus to additional savings/investment optimization | Customer has available capacity |
| `PROTECTION_GAP` | Map to protection/coverage product categories, not investment allocation by default | Protection needs require different product logic |

## 7. Allocation Edge Cases

| Case | Required Behavior |
|---|---|
| Monthly available amount <= 0 | Do not recommend new investment. Return cash-flow improvement and debt-management guidance. |
| Emergency reserve below minimum | Prioritize emergency reserve. Long-term goals may receive only minimum allocation if feasible. |
| High-cost debt exists | Balance minimum emergency floor and high-cost debt repayment before discretionary goals. |
| Urgent goals exceed available amount | Allocate by target date, priority, and feasibility; expose underfunded goals. |
| Multiple diagnosis tags conflict | Apply base priority order and expose tradeoff rationale. |

## 8. Goal Funding Need

```text
monthly_required_amount = (target_amount - current_prepared_amount) / months_until_target
```

Rules:

- If target date is past or current month, mark the goal as immediate/invalid for monthly accumulation.
- If target amount is already met, required amount is `0`.
- Goals are bucketed into `SHORT`, `MID`, and `LONG` by target horizon.

## 9. Product Category Mapping

| Purpose | Product Categories |
|---|---|
| Emergency reserve | high-liquidity cash/deposit products |
| 1-year or shorter goal | short-term stable savings products |
| 1-5 year goal | stable or neutral mid-term products |
| Retirement | long-term pension, savings, tax-benefit products |
| Protection gap | protection/coverage insurance-like products |
| Additional investment | risk-profile-compatible investment products |

## 10. Product Hard Filters

Hard filters always run before scoring. A filtered-out product must not be revived by a high score.

Exclude products when:

- `sale_status != ACTIVE`
- product risk level is clearly incompatible with customer risk profile
- `min_monthly_payment` exceeds allocation monthly amount
- recommended term conflicts with goal horizon
- product purpose tags do not match allocation purpose
- required product document/evidence is missing for RAG-required recommendation contexts

Store exclusion reasons when feasible.

## 11. Product Scoring

After hard filters, score candidates with explainable sub-scores.

| Component | Weight |
|---|---:|
| purpose_fit | 30 |
| term_fit | 20 |
| risk_fit | 20 |
| payment_fit | 15 |
| liquidity_fit | 10 |
| tax_benefit_fit | 5 |

```text
fit_score = Σ(component_score * weight)
```

Persist final score and sub-scores.

## 12. RAG Generation Contract

RAG output must be structured as:

```json
{
  "customer_friendly_reason": "",
  "advisor_reason": "",
  "caution_summary": "",
  "source_document_refs": [],
  "insufficient_evidence_flag": false
}
```

If relevant, current, product-specific source evidence is insufficient, set `insufficient_evidence_flag = true` and do not generate unsupported benefits or claims.

## 13. Report Logic

Customer reports include:

1. financial condition summary
2. key issues
3. proposed allocation
4. product category and product candidate summaries
5. customer-friendly rationale
6. cautions
7. next advisor discussion points

Advisor reports include:

1. original inputs
2. metrics
3. diagnosis tags
4. allocation rationale
5. hard filter and scoring details
6. RAG source summaries
7. manual edit history
