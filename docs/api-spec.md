# API Spec

## 1. API Principles

- Use REST endpoints with noun-based resources.
- Validate all request bodies with Pydantic v2.
- Keep deterministic scoring data separate from generated AI text.
- Return actionable validation errors.
- Paginate list endpoints.
- Write audit logs for generation, manual edit, export, admin, and document events.

## 2. Response Envelope

Use a consistent envelope from the beginning.

```json
{
  "data": {},
  "meta": {},
  "errors": []
}
```

For validation errors:

```json
{
  "data": null,
  "meta": {},
  "errors": [
    {
      "code": "VALIDATION_ERROR",
      "field": "monthly_income_total",
      "message": "monthly_income_total is required"
    }
  ]
}
```

## 3. Endpoint Groups

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

## 4. Core Endpoints

### Auth

| Method | Path | Purpose |
|---|---|---|
| POST | `/auth/login` | Issue advisor/admin token |
| POST | `/auth/logout` | Revoke/session cleanup if applicable |
| GET | `/auth/me` | Current user profile |

### Customers

| Method | Path | Purpose |
|---|---|---|
| GET | `/customers` | Paginated customer list |
| POST | `/customers` | Create customer |
| GET | `/customers/{customer_id}` | Customer detail |
| PATCH | `/customers/{customer_id}` | Update customer |

### Financial Statements

| Method | Path | Purpose |
|---|---|---|
| POST | `/customers/{customer_id}/financial-statements/upload` | Upload standard Excel v1 |
| GET | `/financial-statements/{statement_id}` | Parsed statement detail |
| PATCH | `/financial-statements/{statement_id}` | Manual correction |
| POST | `/financial-statements/{statement_id}/validate` | Re-run validation |

Upload must not proceed as production-ready until the Excel template v1 spec is finalized.

### Goals and Risk Profiles

| Method | Path | Purpose |
|---|---|---|
| POST | `/customers/{customer_id}/goals` | Create goal |
| GET | `/customers/{customer_id}/goals` | List goals |
| PATCH | `/goals/{goal_id}` | Update goal |
| POST | `/customers/{customer_id}/risk-profiles` | Create assessed risk profile |
| GET | `/customers/{customer_id}/risk-profiles/latest` | Latest risk profile |

### Diagnoses

| Method | Path | Purpose |
|---|---|---|
| POST | `/financial-statements/{statement_id}/diagnoses` | Generate deterministic diagnosis |
| GET | `/diagnoses/{diagnosis_id}` | Diagnosis detail |

Diagnosis response must include metrics, tags, structured issues, and deterministic rationales.

### Portfolio Plans

| Method | Path | Purpose |
|---|---|---|
| POST | `/diagnoses/{diagnosis_id}/portfolio-plans` | Generate allocation plan |
| GET | `/portfolio-plans/{portfolio_id}` | Portfolio plan detail |
| PATCH | `/portfolio-plans/{portfolio_id}/allocations/{allocation_id}` | Advisor override |
| POST | `/portfolio-plans/{portfolio_id}/finalize` | Mark final after advisor review |

Manual overrides must store reason and write audit logs.

### Products

| Method | Path | Purpose |
|---|---|---|
| GET | `/products` | Paginated product list |
| POST | `/products` | Create product |
| GET | `/products/{product_id}` | Product detail |
| PATCH | `/products/{product_id}` | Update product |

Admin product writes must audit `ADMIN_PRODUCT_UPDATED`.

### Product Documents

| Method | Path | Purpose |
|---|---|---|
| POST | `/products/{product_id}/documents` | Upload product document |
| GET | `/products/{product_id}/documents` | List documents |
| POST | `/product-documents/{document_id}/index` | Chunk and index document |

Document upload requires version, validity window, sale status snapshot, document type, and source filename.

### Recommendations

| Method | Path | Purpose |
|---|---|---|
| POST | `/portfolio-plans/{portfolio_id}/recommendations` | Generate product recommendations |
| GET | `/recommendations/{recommendation_id}` | Recommendation detail |
| GET | `/portfolio-plans/{portfolio_id}/recommendations` | Recommendation list |

Recommendation responses must separate:

- hard filter results
- score and sub-scores
- deterministic system reason
- generated RAG fields
- source document references
- insufficient evidence flag

### Reports

| Method | Path | Purpose |
|---|---|---|
| POST | `/portfolio-plans/{portfolio_id}/reports/preview` | Build report preview |
| POST | `/portfolio-plans/{portfolio_id}/reports` | Generate PDF report |
| GET | `/reports/{report_id}` | Report metadata |
| GET | `/reports/{report_id}/download` | Download generated PDF |

Report generation must persist `advisor_id`, `generated_by`, `review_status`, and `REPORT_EXPORTED` audit events.

## 5. Authorization Rules

- Advisors can access customers assigned to them.
- Admins can manage product DB and document corpus.
- Reviewers can read plans and audit history when P1 reviewer flow is implemented.
- Customer direct login is out of scope for first MVP.

## 6. Pagination

List endpoints use:

```text
?page=1&page_size=25
```

Response `meta` includes:

```json
{
  "page": 1,
  "page_size": 25,
  "total": 100
}
```
