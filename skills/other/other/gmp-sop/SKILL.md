---
name: gmp-sop
description: >-
  Drafts inspection-ready GMP standard operating procedures for regulated
  manufacturing. Covers document control, role accountability, process controls,
  deviation/CAPA handling, and records management aligned to FDA CGMP (21 CFR
  210/211), Part 11, ICH Q7/Q9/Q10, WHO GMP, PIC/S, and EU GMP. Use when
  creating or overhauling a GMP SOP, preparing for audits or inspections, or
  building compliance-ready procedures. Trigger: GMP, SOP, CGMP, 21 CFR 210,
  21 CFR 211, Part 11, ICH Q7, ICH Q9, ICH Q10, WHO GMP, PIC/S, EU GMP.
---

# GMP Standard Operating Procedure

Produces a GMP-compliant SOP that is inspection-ready and operationally executable.

## Quick Start

1. Gather inputs: process scope, applicable regulations, QMS context, equipment list, record systems.
2. Walk through each SOP section below, filling tables and templates.
3. Mark any unverified citations with `[VERIFY]`.
4. Route for QA review and approval before release.

## Prerequisites

Collect before drafting:

- **Process scope** — product type, dosage form, facility class, target markets
- **Applicable regs** — FDA CGMP, ICH, WHO, PIC/S, EU GMP, local requirements
- **QMS context** — document numbering, approval matrix, related SOPs
- **Equipment** — asset IDs, calibration/maintenance/qualification status
- **Record systems** — paper vs electronic, Part 11 status
- **Inspection history** — FDA 483s, warning letters, open CAPAs
- **SME/approver list** — production, QA, QC, engineering, management

## SOP Sections

### 1. Document Control Page

| Field | Content |
|---|---|
| SOP Title | Precise scope (process/area) |
| SOP ID | Site numbering convention |
| Version | Numeric or semantic |
| Effective Date | Approved use date |
| Supersedes | Prior SOP ID/version |
| Prepared By | Name, role, date |
| Reviewed By | QA, SMEs |
| Approved By | QA/Management |
| Distribution | Controlled locations |
| Related SOPs | IDs and titles |
| Electronic Signatures | Part 11 status |

### 2. Purpose and Scope

```
Purpose:
This SOP establishes controlled steps for [process] to ensure GMP compliance under [reg citations].

Scope:
Applies to [areas, equipment, product types, personnel]. Excludes [exclusions with rationale].
Interfaces: [related SOP IDs].
```

### 3. Regulatory Basis

List only applicable regulations. Use `[VERIFY]` for unconfirmed citations.

| Authority | Citation |
|---|---|
| FDA CGMP | 21 CFR Parts 210/211 |
| Electronic records | 21 CFR Part 11 |
| ICH | Q7 (API), Q9, Q10 |
| WHO | TRS GMP guidance |
| PIC/S | GMP Guide |
| EU | EU GMP Guide + Annexes |

### 4. Definitions

Provide GMP-aligned definitions consistent with site QMS. Minimum set: CPP, CQA, deviation, OOS, OOT, batch record, validation, qualification, calibration.

### 5. Responsibilities Matrix

| Role | Duties | Decisions/Approvals | Records Owned |
|---|---|---|---|
| Production | Execute SOP steps | Stop work for deviations | Batch records |
| QA | Approve SOP, review deviations | Release/closure authority | QA review logs |
| QC | Testing, sampling | OOS disposition | Lab records |
| Engineering | Maintenance/calibration | Equipment readiness | PM/calibration logs |
| Management | Resource allocation | Final approval | Training matrix |

### 6. Materials, Equipment, and Utilities

| Item | ID/Spec | Qualification | Calibration/PM | Acceptance Criteria |
|---|---|---|---|---|
| Equipment | Asset ID | IQ/OQ/PQ status | Frequency | Tolerance |
| Materials | Grade/spec | Supplier status | Storage | COA required |
| Utilities | Water/HVAC/gases | Monitoring | Limits | Action levels |

### 7. Procedure Steps

Each step must specify role, action, records, and acceptance criteria.

| Step | Role | Action | CPP/CQA | Hold Point | Records |
|---|---|---|---|---|---|
| 1 | Production | [imperative action] | [range] | QA if required | [record] |
| 2 | QC | [sample/test] | [spec] | QA review | [record] |
| 3 | QA | [verification] | N/A | Release | [record] |

Step rules:
- Include decision points and stop-work criteria
- Define acceptance ranges for all CPPs/CQAs
- State required PPE/cleanroom behavior where applicable
- Require documentation at time of action (concurrent recording)

### 8. In-Process Controls

| Control | Frequency | Method | Acceptance | Action if OOR |
|---|---|---|---|---|
| [Control] | [per batch/time] | [method] | [spec] | [action] |

### 9. Deviations, OOS/OOT, and CAPA

- Document deviation within same shift or defined timeframe
- Quarantine affected material/lots
- Initiate root cause investigation
- Assess impact on product quality and patient safety
- Implement CAPA with effectiveness checks
- Document QA disposition and release decision

### 10. Documentation and Records

| Record | Owner | System | Review Timeline | Retention |
|---|---|---|---|---|
| Batch record | Production | Paper/eQMS | [timeframe] | Per 21 CFR 211.180 `[VERIFY]` |
| Calibration log | Engineering | Paper/eQMS | [timeframe] | [policy] |
| Training record | QA/HR | LMS/eQMS | [timeframe] | [policy] |

If electronic: require validation, audit trails, access control, e-signatures per Part 11.

### 11. Training and Qualification

- Initial training before first execution
- Retraining on each revision
- Qualification for roles with critical steps
- Document training effectiveness

### 12. Change Control and Revision History

| Version | Effective Date | Change Summary | Rationale | Approvers |
|---|---|---|---|---|
| 1.0 | [date] | Initial release | [reason] | [names] |

### 13. References

List all cited standards with version/date. Mark uncertain items `[VERIFY]`.

### 14. Appendices

Include controlled templates: SOP execution checklist, batch record template, deviation report template, in-process control log, equipment cleaning log.

## Pitfalls and Checks

- **Language** — use imperative, unambiguous phrasing; never advisory ("should consider")
- **Citations** — verify all regulatory citations are current; mark uncertain ones `[VERIFY]`
- **Role segregation** — maintain separation between production and QA/QC functions
- **Retention** — apply the strictest applicable retention requirement across jurisdictions
- **Jurisdiction** — add annexes for non-U.S. markets (EU, WHO, PIC/S requirements)
- **Part 11** — confirm electronic record controls whenever eQMS or e-signatures are used
