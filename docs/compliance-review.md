# Compliance Review

## 1. Purpose

This document defines the legal and regulatory review areas that must be addressed before FinRoute is released as a production MVP. It is not a legal opinion. Final interpretation must come from qualified legal/compliance reviewers.

## 2. Release Gate

MVP release requires a documented legal/regulatory review result that covers:

1. Capital Markets Act applicability
2. Financial Consumer Protection Act applicability
3. Whether generated product rationale may be interpreted as investment solicitation or investment advisory content
4. Suitability and appropriateness process requirements
5. Explanation duty and customer-facing disclosure requirements
6. Record retention and audit requirements
7. Required disclaimers and advisor approval language

Parser, product recommendation, RAG rationale, and report export can be prototyped, but production use must not be approved until this review is complete.

## 3. Key Risk Areas

| Area | Review Question | Product Impact |
|---|---|---|
| Investment solicitation | Can generated product recommendations be treated as solicitation? | May require stricter approval, wording, and record controls |
| Investment advisory | Does automated portfolio allocation create advisory obligations? | May affect licensing and disclosure |
| Suitability/appropriateness | Does risk-profile capture satisfy required standards? | May require questionnaire, scoring, and signed records |
| Explanation duty | Are product risks and cautions sufficiently surfaced? | Must influence report template and UI |
| Advisor review | Is advisor approval enough for intended use? | Treat as control, not immunity |
| RAG evidence | Are product claims traceable to approved documents? | Requires citation, version, and validity tracking |
| Audit retention | What records must be retained and for how long? | Affects audit schema and storage policy |

## 4. Required Product Controls

- Product recommendation outputs must show deterministic filter/scoring reasons.
- RAG-generated text must include source references or an insufficient-evidence warning.
- Customer-facing proposal reports must distinguish system-generated draft content from advisor-reviewed final content.
- Advisor manual edits must capture before/after values and rationale.
- Reports must record `advisor_id`, `generated_by`, report type, status, and timestamp.
- Sale-stopped or outdated product documents must not be used as current supporting evidence.

## 5. Required UX/Copy Review

The following text categories require legal/compliance review before production:

- Product recommendation explanations
- Risk and caution summaries
- Customer-facing disclaimers
- Advisor approval labels
- Report finalization language
- Insufficient evidence warning language

## 6. MVP Compliance Checklist

| Item | Required Before MVP Release |
|---|---|
| Legal review owner assigned | Yes |
| Regulatory scope memo completed | Yes |
| Advisor review flow approved | Yes |
| Report disclaimer approved | Yes |
| Suitability/risk profile process approved | Yes |
| Audit retention policy approved | Yes |
| RAG evidence and citation policy approved | Yes |

## 7. Non-Goals

The MVP does not implement a full autonomous compliance engine. It implements traceability, review controls, source-grounded explanations, and audit records to support advisor and compliance workflows.
