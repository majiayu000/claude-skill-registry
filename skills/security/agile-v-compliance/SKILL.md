---
name: agile-v-compliance
description: Risk management, CAPA protocol, human gate approval records, AI agent security controls, and periodic revalidation. Load when running gates, auditing risks, handling CAPAs, or reviewing security posture.
license: CC-BY-SA-4.0
metadata:
  version: "1.3"
  standard: "Agile V"
  compliance: "ISO 9001 6.1, ISO 13485 8.5, ISO 27001 A.5.23/A.8.3, 21 CFR Part 11, GxP/GAMP 5"
  author: agile-v.org
---

# Instructions

Compliance protocols for Agile V. Requires **agile-v-core** loaded first.

## Risk Management (ISO 9001 6.1 / AS9100D 8.1.1)

Append-only, cycle-tagged register in `.agile-v/RISK_REGISTER.md`: `RISK-ID | Cycle | Category | Description | Likelihood | Impact | Severity | Mitigation | Owner | Status`

**Categories:** Technical, Process, Compliance, Security. **Severity matrix:** High x High = Critical, High x Med = High, High x Low / Med x Med = Medium, rest = Low. Critical risks require Human resolution or documented acceptance before Gate 2.

**When:** Stage 1 = Req Architect identifies. Stage 2 = Logic Gatekeeper flags constraints. Stage 4 = Red Team finds residual. Cycle boundary = Compliance Auditor reviews.

## CAPA Protocol (ISO 13485 8.5 / ISO 9001 10.1-10.2)

**Triggers:** CRITICAL finding, recurring NC across cycles, regression FAIL with no CR, 3-attempt escalation.

Record in `.agile-v/CAPA_LOG.md`: `CAPA-XXXX` with Cycle, Trigger, Nonconformity, Root Cause (5-Whys), Corrective Action, Preventive Action, Effectiveness Verification, Status (open -> corrective-complete -> preventive-complete -> verified-effective -> closed), Owner.

**Workflow:** Detect -> Record -> Analyze -> Correct -> Prevent -> Verify effectiveness. Compliance Auditor tracks open CAPAs at Gate 2, flags overdue (>2 cycles).

## Human Gate Approval Records (21 CFR Part 11 / Annex 11)

Append-only in `.agile-v/APPROVALS.md`: `GATE-XXXX` with Gate type, Cycle, Scope, Decision (Approved/Conditional/Rejected), Conditions, Approver (full name), Role/Authority, Timestamp (ISO 8601), Signature Method, Evidence Reference (commit hash).

**Rules:** Name + role required (not just "Human"). Authority from matrix in config.json. Rejected = pipeline halts.

| Regulatory Context | Minimum Signature |
|---|---|
| Non-regulated | APPROVALS.md entry with name + timestamp |
| ISO 9001/27001 | + Git commit attribution |
| GxP / 21 CFR Part 11 | + Signed commit + authority verification |
| ISO 13485 | + Digital signature + authority matrix + retention |

## AI Agent Security Controls (ISO 27001 A.5.23 / A.8.3)

**LLM Provider Registry** in config.json: per provider record name, models, data_residency, retention, api_data_usage, approved_for classifications, review_date. Verify input classification vs provider approval before sending. Never send credentials/patient data unless provider approved. Least privilege per agent. Context sanitization on session end.

**File Integrity:** Git-tracked = verify clean status. Store hashes in STATE.md at Gates; verify before next stage. Flag unverifiable files to Human.

## Periodic Review & Revalidation (GxP / GAMP 5)

**Triggers:** LLM model change, runtime/platform major update, skill file change, >5 CRs since last revalidation, 12-month interval.

Record in `.agile-v/REVALIDATION_LOG.md`: `REVAL-XXXX` with Date, Trigger, Scope, Results, Decision, Reviewer. Regression failure = new cycle trigger.

**Model Tracking** in config.json: model_versions with tier IDs + last_validated + validated_by. Any change triggers revalidation.
