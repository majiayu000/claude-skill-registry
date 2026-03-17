---
name: incoherence
description: Detect contradictions between documentation and code, ambiguous specs,
  and policy violations across a codebase. Use when documentation seems stale,
  specs conflict with implementation, or a pre-release consistency audit is needed.
  Produces an actionable incoherence report with resolution workflow.
license: MIT
metadata:
version: 1.0.0
model: claude-sonnet-4-5
---

# Incoherence Detector Skill

## Purpose

Detect and resolve incoherence: contradictions between docs and code, ambiguous specifications, missing documentation, or policy violations.

## Triggers

| Trigger Phrase | Operation |
|----------------|-----------|
| `find contradictions in the docs` | Detection phase (steps 1-13) |
| `audit docs vs code consistency` | Detection phase with Dimension A focus |
| `check for stale documentation` | Detection phase with Dimension D focus |
| `run incoherence detector` | Full detection phase |
| `reconcile incoherence report` | Reconciliation phase (steps 14-22) |

---

## When to Use

Use this skill when:

- Documentation may contradict actual code behavior
- Preparing for a release and need a consistency audit
- Specs have changed but implementation status is unclear
- Multiple authors edited docs and code independently

Use direct code review instead when:

- Investigating a single known bug
- The inconsistency is already identified and just needs a fix

---

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Skipping the report filename specification | Script requires output path upfront | Specify filename before starting detection |
| Running reconciliation without user edits | Nothing to apply, wasted steps | Wait for user to fill Resolution sections |
| Editing the report format manually | Breaks reconciliation parsing | Let the script manage report structure |
| Selecting all 11 dimensions | Excessive scope, diminishing returns | Let step 2 select the most relevant 3-5 |
| Ignoring low-severity issues | They accumulate into real drift | Triage all issues, defer explicitly if needed |

---

## Verification

After detection:

- [ ] Report file created at user-specified path
- [ ] Each issue has Type, Severity, Source A/B, Suggestions, and Resolution section
- [ ] Dimension coverage matches selection from step 2

After reconciliation:

- [ ] Resolved issues show status marker in report
- [ ] Code changes match user-provided resolutions
- [ ] No unresolved critical or high severity issues remain

---

## Prerequisites

**Before starting**: User must specify the report filename (e.g., "output to incoherence-report.md").

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/incoherence.py` | 22-step detection and reconciliation workflow for doc-code contradictions |

## Invocation

```bash
# Detection phase (steps 1-13)
python3 scripts/incoherence.py --step-number 1 --total-steps 22 --thoughts "<context>"

# Reconciliation phase (steps 14-22, after user edits report)
python3 scripts/incoherence.py --step-number 14 --total-steps 22 --thoughts "Reconciling..."
```

## Process

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
