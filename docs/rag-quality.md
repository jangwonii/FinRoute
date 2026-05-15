# RAG Quality

## 1. Purpose

This document defines the minimum RAG design and quality requirements for product-document-grounded explanations.

RAG must explain deterministic recommendations. It must not decide allocations, suitability, or final product eligibility by itself.

## 2. Required Metadata

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

## 3. Retrieval Rules

- Filter by selected product candidate before semantic retrieval when generating product-specific rationale.
- Prefer `ACTIVE` products and current valid document versions.
- Exclude expired documents unless the UI explicitly labels them as historical.
- Do not mix outdated and current versions without clearly separating them.
- Return source refs with document ID, filename, version, and chunk index.

## 4. Prompt Requirements

Prompt templates must be versioned. Each template should specify:

- template ID and version
- target audience: customer or advisor
- allowed source context
- required output schema
- refusal/insufficient-evidence behavior
- citation/source-ref requirement

Generated output must follow:

```json
{
  "customer_friendly_reason": "",
  "advisor_reason": "",
  "caution_summary": "",
  "source_document_refs": [],
  "insufficient_evidence_flag": false
}
```

## 5. Insufficient Evidence Rules

Set `insufficient_evidence_flag = true` when:

- no current product-specific document chunk is retrieved
- retrieved chunks do not support the requested claim
- source refs are missing
- retrieved documents are expired or sale-stopped and no current replacement is available
- generated text includes benefits, conditions, or cautions not supported by retrieved documents

When the flag is true, do not generate unsupported recommendation claims. Return a concise message that product-document evidence is insufficient.

## 6. UI Requirements

The UI must show:

- a warning badge for insufficient evidence
- the text `문서 근거 부족`
- source document refs for supported claims
- document version and filename in advisor-facing views

Customer-facing views may show simplified source labels, but advisor-facing views must retain traceability.

## 7. Evaluation Metrics

Evaluate RAG with fixture products and documents.

| Metric | Meaning |
|---|---|
| source coverage | required product/document evidence is retrieved |
| citation presence | generated claims include source refs |
| faithfulness | generated text is supported by retrieved chunks |
| insufficient evidence precision | unsupported cases are correctly flagged |
| outdated document exclusion | expired/sale-stopped documents are excluded from current evidence |

## 8. Minimum Test Cases

- Product has no documents: insufficient evidence.
- Product has only expired documents: insufficient evidence or historical-only label.
- Product has active document but no relevant chunk: insufficient evidence.
- Product has relevant current document: generated rationale includes source refs.
- Source refs missing from model response: response is rejected or regenerated.
- Customer and advisor explanations are separated.
- Caution summary is generated only from supported document content.

## 9. Operational Notes

- RAG quality depends on product document freshness.
- Document upload ownership must be assigned before MVP launch.
- Product documents should be reviewed after product DB changes.
- Prompt changes should be versioned and test fixtures rerun.
