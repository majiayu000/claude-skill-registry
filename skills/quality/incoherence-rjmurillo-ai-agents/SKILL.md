---
name: incoherence
description: Detect and resolve incoherence in documentation, code, specs vs implementation. Includes reconciliation phase for applying user-provided resolutions.
license: MIT
metadata:
version: 1.0.0
model: claude-sonnet-4-5
---

# Incoherence Detector Skill

## Purpose

Detect and resolve incoherence: contradictions between docs and code, ambiguous specifications, missing documentation, or policy violations.

## Prerequisites

**Before starting**: User must specify the report filename (e.g., "output to incoherence-report.md").

## Invocation

```bash
# Detection phase (steps 1-13)
python3 scripts/incoherence.py --step-number 1 --total-steps 22 --thoughts "<context>"

# Reconciliation phase (steps 14-22, after user edits report)
python3 scripts/incoherence.py --step-number 14 --total-steps 22 --thoughts "Reconciling..."
```

## Workflow (22 Steps)

```
DETECTION PHASE (Steps 1-13):

Step 1:  CODEBASE SURVEY          ─────┐
Step 2:  DIMENSION SELECTION           │ Parent
Step 3:  EXPLORATION DISPATCH     ─────┘
         │
         ▼
    ┌────────────────────────┐
    │ Step 4:  BROAD SWEEP   │
    │ Step 5:  COVERAGE CHECK│ Exploration
    │ Step 6:  GAP-FILL      │ Sub-agents
    │ Step 7:  FORMAT        │
    └────────────────────────┘
         │
         ▼
Step 8:  SYNTHESIS                ─────┐
Step 9:  DEEP-DIVE DISPATCH       ─────┘ Parent
         │
         ▼
    ┌────────────────────────┐
    │ Step 10: EXPLORATION   │ Deep-dive
    │ Step 11: FORMAT        │ Sub-agents
    └────────────────────────┘
         │
         ▼
Step 12: VERDICT ANALYSIS         ─────┐
Step 13: REPORT GENERATION             │ Parent
         │                        ─────┘
         ▼
    ═══════════════════════════
    USER EDITS REPORT
    (fills in Resolution sections)
    ═══════════════════════════
         │
         ▼
RECONCILIATION PHASE (Steps 14-22):

Step 14: RECONCILE PARSE          ─────┐
Step 15: RECONCILE ANALYZE             │
Step 16: RECONCILE PLAN                │ Parent
Step 17: RECONCILE DISPATCH       ─────┘
         │
         ▼
    ┌────────────────────────┐
    │ Step 18: APPLY         │ Sub-agents
    │ Step 19: FORMAT        │ (invoke script)
    └────────────────────────┘
         │
         ▼
Step 20: RECONCILE COLLECT        ───┐
         │ (loop if more waves)      │
         ▼                           │ Parent
Step 21: RECONCILE UPDATE            │
         │                           │
         ▼                           │
Step 22: RECONCILE COMPLETE      ────┘
```

## Reconciliation Behavior

**Idempotent**: Can be run multiple times on the same report.

**Skip conditions** (issue left unchanged):

- No resolution provided by user
- Already marked as resolved (from previous run)
- Could not apply (sub-agent failed)

**Only action**: Mark successfully applied resolutions as ✅ RESOLVED in report.

## Report Format

Step 9 generates issues with Resolution sections:

```markdown
### Issue I1: [Title]

**Type**: Contradiction | Ambiguity | Gap | Policy Violation
**Severity**: critical | high | medium | low

#### Source A / Source B

[quotes and locations]

#### Suggestions

1. [Option A]
2. [Option B]

#### Resolution

<!-- USER: Write your decision below. Be specific. -->

<!-- /Resolution -->
```

After reconciliation, resolved issues get a Status section:

```markdown
#### Resolution

<!-- USER: Write your decision below. Be specific. -->

Use the spec value (100MB).

<!-- /Resolution -->

#### Status

✅ RESOLVED — src/uploader.py:156: Changed MAX_FILE_SIZE to 100MB
```

## Dimension Catalog (A-K)

| Cat | Name                              | Detects                                 |
| --- | --------------------------------- | --------------------------------------- |
| A   | Specification vs Behavior         | Docs vs code                            |
| B   | Interface Contract Integrity      | Types/schemas vs runtime                |
| C   | Cross-Reference Consistency       | Doc vs doc                              |
| D   | Temporal Consistency              | Stale references                        |
| E   | Error Handling Consistency        | Error docs vs implementation            |
| F   | Configuration & Environment       | Config docs vs code                     |
| G   | Ambiguity & Underspecification    | Vague specs                             |
| H   | Policy & Convention Compliance    | ADRs/style guides violated              |
| I   | Completeness & Documentation Gaps | Missing docs                            |
| J   | Compositional Consistency         | Claims valid alone, impossible together |
| K   | Implicit Contract Integrity       | Names/messages that lie about behavior  |
