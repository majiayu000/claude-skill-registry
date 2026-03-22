---
name: gdpr-dpa
description: >-
  Drafts GDPR Article 28-compliant Data Processing Addenda with schedules
  ready for execution. Use when drafting or updating a DPA, vendor GDPR
  addendum, controller-processor agreement, or data protection addendum
  involving sub-processors, breach notification, audits, international
  transfers, or SCCs.
---

# GDPR Data Processing Addendum (DPA)

Produces an Article 28-compliant DPA aligned with the governing service agreement, covering processing details, security, sub-processor controls, breach notice, audits, and deletion terms.

## Quick Start

Gather before drafting:

- [ ] Party details: legal names, addresses, registration numbers (Controller + Processor)
- [ ] Underlying agreement reference (name, date, SOWs/order forms)
- [ ] Processing description: subject matter, duration, nature, purpose, operations
- [ ] Data inventory: data subject categories, personal data types, special categories (Art 9), criminal data (Art 10)
- [ ] Transfer map: processing locations, transfer mechanism (adequacy, SCCs, BCRs, Art 49)
- [ ] Security baseline: certifications, TOMs
- [ ] Sub-processor list + approval model (general vs specific) with objection window
- [ ] Incident response SLAs and audit preferences
- [ ] Termination: return/deletion formats, timelines, retention constraints

## Drafting Workflow

1. Draft header, recitals, effective date, and order-of-precedence clause with the main agreement.
2. Define GDPR terms: Controller, Processor, Personal Data, Processing, Sub-processor, Data Protection Laws, Personal Data Breach, Services.
3. Insert Article 28(3) mandatory clauses (see checklist below).
4. Add security (Art 32), breach notification (Arts 33-34), and assistance (Arts 32-36) clauses.
5. Add sub-processor governance (Art 28(2), 28(4)) with flow-down obligations.
6. Add audit and compliance evidence provisions (Arts 28(3)(h), 40, 42).
7. If data leaves the EEA, add international transfer terms (Art 46 SCCs, Art 47 BCRs, Art 49 derogations).
8. Add termination, return/deletion obligations, and backup handling.
9. Populate Schedules A-D from inputs; mark gaps as `[REQUIRED]`.

## Article 28(3) Mandatory Clause Checklist

| GDPR basis | Clause | Required content |
|---|---|---|
| Art 28(3)(a) | Instructions | Process only on documented Controller instructions; notify if instruction violates law |
| Art 28(3)(b) | Confidentiality | Authorized personnel bound by confidentiality |
| Art 28(3)(c) | Security | Appropriate TOMs per Art 32 |
| Art 28(3)(d) | Sub-processors | No sub-processing without authorization; flow-down equivalent obligations |
| Art 28(3)(e) | Data subject rights | Assist Controller with Chapter III requests |
| Art 28(3)(f) | Assistance | Assist with Art 32-36 obligations including DPIA and prior consultation |
| Art 28(3)(g) | Return/Deletion | Return or delete personal data at end of services; certify |
| Art 28(3)(h) | Audits/Info | Make information available; allow and contribute to audits |

## Key Decision Points

| Decision | Options | Input needed |
|---|---|---|
| Sub-processor authorization | General / Specific | Controller policy, objection window |
| Audit model | On-site / Remote / Third-party / Certification | Vendor policy, existing reports |
| Breach notice SLA | 24h / 48h / Other | Risk tolerance, incident playbooks |
| Data return format | CSV / JSON / Native export | System compatibility |
| Transfer mechanism | Adequacy / SCCs / BCRs / Art 49 | Data flows and locations |

## Schedule Templates

**Schedule A — Approved Sub-processors**

| Name | Location | Processing Activity | Authorization Type | Notice Period |
|---|---|---|---|---|
| TBD | TBD | TBD | General/Specific | 30 days |

**Schedule B — Description of Processing**

| Field | Details |
|---|---|
| Subject matter | |
| Duration | |
| Nature of processing | |
| Purpose | |
| Processing operations | |
| Categories of data subjects | |
| Categories of personal data | |
| Special categories (Art 9) | |
| Criminal data (Art 10) | |
| Processing locations | |

**Schedule C — Technical and Organizational Measures**

| Domain | Measures |
|---|---|
| Access control | |
| Encryption/pseudonymization | |
| Logging/monitoring | |
| Availability/resilience | |
| Incident response | |
| Testing/evaluation | |
| Physical security | |

**Schedule D — Audit/Certification Evidence**

| Evidence | Date | Scope | Reference |
|---|---|---|---|
| ISO 27001 | | | |
| SOC 2 Type II | | | |

## Pitfalls

- **No absolute security promises.** Use "appropriate" measures per Art 32; tie to risk profile.
- **Special categories / children's data** require heightened safeguards and stricter access controls.
- **Missing transfer basis is a blocker.** If any non-EEA transfer occurs, specify the mechanism and attach SCCs or equivalent before finalizing.
- **Schedule consistency.** Keep schedules aligned with DPA body text; ensure sub-processor lists are current.
- **Order of precedence.** Data protection terms must prevail over conflicting service agreement terms.
- Mark uncertain legal citations with `[VERIFY]`.
