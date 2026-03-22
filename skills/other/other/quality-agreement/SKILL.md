---
name: quality-agreement
description: Drafts Quality Agreements for pharmaceutical contract manufacturing. Assigns quality roles between product owners and CMOs under FDA cGMP (21 CFR 210/211), ICH Q7, and related guidance. Use when a user needs a quality agreement, CMO quality terms, or cGMP compliance agreement for contract manufacturing.
tags:
  - agreement
  - drafting
  - regulatory
---

# Quality Agreement for Contract Manufacturing

Drafts an enforceable Quality Agreement defining quality roles, responsibilities, and cGMP compliance obligations between a product owner and a contract manufacturing organization (CMO).

## Prerequisites

1. **Manufacturing/supply agreement** — commercial terms, product scope, facility details
2. **Regulatory identifiers** — FDA Establishment IDs, DUNS, DEA registrations (if controlled), ISO certs
3. **Product details** — dosage form, API/finished product, classification (Rx, OTC, biologic)
4. **Existing quality documents** — prior quality agreements, SOPs, inspection history (483s, warning letters)
5. **Specifications** — approved specs, analytical methods, stability protocols

Search user-uploaded documents for existing agreements, specs, and regulatory correspondence before drafting.

## Output Structure

| Section | Key Contents |
|---------|-------------|
| Parties & Scope | Legal names, regulatory IDs, product scope, exclusions, quality-over-commercial supremacy clause |
| Definitions | Regulatory terms, party-specific roles |
| Quality Unit Authority | Responsibility matrix (see below), independence provisions, escalation paths |
| Manufacturing & Documentation | Batch records, retention per 21 CFR 211.180, Part 11 compliance |
| Change Control | Categories, approval workflows, review timelines (see below) |
| Audit & Inspection | Routine/for-cause/unannounced rights, 483 response coordination |
| Quality Events & CAPA | Deviation reporting, investigation, CAPA approval, recall authority |
| Specifications & Release | Method validation (ICH Q2), OOS investigations, stability programs |
| Personnel & Training | Qualifications, training programs, key personnel change notice |
| Term & Termination | Duration, termination rights, transition obligations, survival clauses |
| Appendices | Change control forms, deviation templates, quality metrics, contacts |

### Quality Unit Responsibility Matrix

| Function | Product Owner | CMO |
|----------|:---:|:---:|
| Final batch disposition | ● | |
| In-process controls execution | | ● |
| Specification approval | ● | |
| Deviation investigation | | ● |
| Deviation report approval | ● | |
| Regulatory submissions | ● | |
| Environmental monitoring | | ● |
| Equipment qualification | | ● |
| Change control approval (major) | ● | |
| Complaint handling (mfg-related) | | ● |
| Recall decision authority | ● | |

### Notification Timelines

| Event | Deadline |
|-------|----------|
| Critical quality event (safety/regulatory) | 24 hours |
| Significant quality event | 72 hours |
| Routine quality event | 5 business days |
| Unannounced regulatory inspection | 4 hours |
| Announced regulatory inspection | 24 hours |
| Key personnel change | 30 days advance |

### Change Control Framework

| Category | Examples | Approval | Review Period |
|----------|----------|----------|---------------|
| Minor | Admin SOP updates, like-for-like equipment | CMO QU (notify owner) | 15 business days |
| Major | Critical process params, alt. suppliers, method revisions | Product owner QU written approval | 30 business days |
| Emergency | Immediate safety/compliance | CMO implements → retrospective owner approval | Immediate |

Change proposals must include: description, scientific justification, risk assessment (FMEA/ICH Q9), validation protocols if applicable, regulatory impact analysis, implementation timeline.

### Audit Rights

- **Pre-approval** — before manufacturing initiation
- **Routine** — ≤24-month intervals, 30 days advance notice
- **For-cause** — triggered by quality events or regulatory concerns
- **Unannounced** — preserved right for serious quality/regulatory concerns
- **Scope** — unrestricted access to batch records, validation reports, deviations, training records, personnel interviews, facility inspection
- **Post-audit** — report within 30 days; CMO CAPA response within 15 business days

### Batch Records & Documentation

- Contemporaneous recording (indelible ink or validated electronic systems)
- Complete material genealogy and traceability
- CMO initial review: 5–10 business days post-batch completion
- Product owner QU review: 10–15 additional business days before disposition
- Retention: ≥1 year past expiry or 3 years post-distribution (whichever longer) per 21 CFR 211.180
- Part 11 compliance: system validation, audit trails, data integrity controls

### Termination & Transition

- **Non-renewal notice**: ≥180 days before term expiry
- **Material breach cure**: 60 days from written notice
- **Convenience termination**: 180–360 days advance notice
- **Post-termination**: CMO supports product through shelf life (stability, reserve samples, complaints, inspections)
- **Document transfer**: Complete batch records and quality documentation within 90 days
- **Survival**: Confidentiality (indefinite), record retention (regulatory periods), regulatory support (while product in distribution)

## Guidelines

- Use mandatory language ("shall," "must") — never aspirational ("should," "will")
- Include explicit quality-over-commercial supremacy clause; quality decisions independent from commercial considerations
- Align with FDA 2016 Guidance: Contract Manufacturing Arrangements for Drugs: Quality Agreements [VERIFY]
- Address data integrity per FDA 2018 Data Integrity and Compliance with Drug CGMP guidance [VERIFY]
- For international markets, incorporate ICH Q7, EU GMP Annex 11, WHO guidelines as applicable
- Include cybersecurity provisions for manufacturing systems and confidential regulatory data
- Quality agreement governs all quality matters; ensure no conflict with underlying supply agreement
- If user provides 483s or warning letters, incorporate preventive measures addressing cited deficiencies
