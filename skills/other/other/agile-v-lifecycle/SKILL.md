---
name: agile-v-lifecycle
description: Multi-cycle iteration management, document versioning, change requests, re-entry points, archival, and impact analysis. Load when starting a new cycle (C2+), processing change requests, or managing cross-cycle traceability.
license: CC-BY-SA-4.0
metadata:
  version: "1.3"
  standard: "Agile V"
  author: agile-v.org
---

# Instructions

Multi-cycle lifecycle management for Agile V. Requires **agile-v-core** loaded first.

## Cycle ID

`C1`, `C2`, ... -- recorded in STATE.md, propagated to all artifact IDs.

## Document Versioning

| Document | Rule | Example |
|---|---|---|
| REQUIREMENTS.md | Revision header + per-REQ status | `<!-- Revision: C2 -->` |
| BUILD_MANIFEST.md | ART-XXXX.N suffix | ART-0001.2 |
| TEST_SPEC.md | TC origin cycle | TC-0001 [C1] |
| VALIDATION_SUMMARY.md | One per cycle; prior archived | VALIDATION_SUMMARY_C1.md |
| DECISION_LOG.md | Cycle-tagged entries | [C2] DECISION: ... |
| ATM.md | Partitioned by cycle | See compliance-auditor |

## REQ Status Tags

`approved [Cn]` | `modified [Cn]` (was/now + CR ref) | `new [Cn]` | `deprecated [Cn]` | `superseded [Cn]`

## Change Requests

Append-only in CHANGE_LOG.md. Format: `CR-XXXX` with Cycle, Affected REQ, Change, Rationale, Impact (ART + TC), Requested by, Approved status. Flow: Req Architect creates -> Logic Gatekeeper validates -> Human approves at Gate 1.

## Cycle Triggers

(1) New feature request. (2) Verification failure requiring REQ change. (3) Approved CR invalidating artifacts. (4) Scheduled iteration. All require Human decision.

## Re-Entry Points

| Trigger | Re-Entry | Scope |
|---|---|---|
| New feature | Stage 1 | Full pipeline new REQs; regression unchanged |
| REQ change from verification | Stage 1 | CR -> Gate 1 -> full affected; regression others |
| Bug fix (no REQ change) | Stage 3 | Build fixes; re-verify affected only |
| Scheduled | Stage 1 | Review all; full for changes; regression stable |

## Archival

On Gate 2 acceptance: snapshot living docs -> `.agile-v/cycles/CN/` (frozen). Never modify archives. DECISION_LOG and CHANGE_LOG never archived -- append-only timeline.

## Impact Analysis (per agent)

(1) Req Architect: tag REQs new/modified/deprecated/unchanged. (2) Logic Gatekeeper: re-validate new+modified only. (3) Build Agent: rebuild modified only; carry forward unchanged. (4) Test Designer: delta tests for new/modified; regression baseline for unchanged. (5) Red Team: execute delta + regression separately. (6) Compliance Auditor: cycle-tag ATM; flag unupdated links.
