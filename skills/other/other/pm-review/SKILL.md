---
name: pm-review
description: Quality review of individual decisions or decision registers. Checks schema compliance, body quality, connection completeness, and staleness. Not a content audit — a structural and reasoning audit. Triggers on "/pm-review", "/pm-review [decision]", "review this decision", "check quality", "audit decisions".
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
context: fork
---

## Runtime Configuration (Step 0)

Read `ops/derivation-manifest.md` for vocabulary mapping.
Read `ops/config.yaml` for stale thresholds and review standards.

---

## EXECUTE NOW

**Target: $ARGUMENTS**

Parse immediately:
- If target contains decision name or path: review that specific decision
- If target is a register name: review all decisions in that register
- If target is empty: review the 10 most recently modified decisions
- If target is "all": review all decisions (slow — use sparingly)

**START NOW.**

---

## Philosophy

**A decision system is only as good as the decisions in it. Bad decisions corrupt the graph.**

The worst failure mode is not missing decisions — it is having decisions that appear well-formed but contain reasoning errors, unverified claims, or stale status. These poison future inference: the PM will act on bad information and not know it.

/pm-review is not editorial judgment about whether a decision is correct. It is a structural and quality audit: does the decision note meet the standards that make it trustworthy? Does the body show reasoning or just assertion? Is the status still accurate? Are the connections correct?

A decision that fails review should be fixed or flagged — not silently retained.

---

## Review Dimensions

### 1. Schema Compliance

Every decision note must have all required fields:
- `description`: present, ≤200 chars, adds info beyond title
- `type`: valid enum value
- `status`: valid enum value
- `meta_state`: valid enum value
- `last_reviewed`: valid date (not YYYY-MM-DD placeholder)
- `topics`: at least one decision register linked

```bash
# Find decisions with placeholder dates
rg "last_reviewed: YYYY-MM-DD" decisions/ --include="*.md" -l

# Find decisions missing required fields
rg "^description: \"\"" decisions/ --include="*.md" -l
```

### 2. Title Quality (Claim Test)

The title must be a claim that can be completed: "This decision argues that [title]."

**Pass:** "QFTest interpreter requires Groovy not groovy casing"
**Pass:** "Vision Client architecture requires 3-phase redesign before QFTest integration"
**Fail:** "QFTest casing issue"
**Fail:** "Sprint 3 decisions"
**Fail:** "Architecture notes"

### 3. Body Quality (Reasoning Test)

The body must show reasoning, not just assert conclusions.

**Required elements:**
- At least one connective word: because, but, therefore, which means, however, since
- Some acknowledgment of the path to the conclusion
- For tech-facts: the validation source (what confirmed this)
- For enforcement: the specific failure that generated this lesson
- For architectural: the alternatives considered (even briefly)

**Length:** 150-400 words. Too short = assertion. Too long = essay.

### 4. Connection Completeness

Does the decision have the connections it should have?
- Tech-fact decisions should connect to the sprint that discovered them
- Enforcement decisions should connect to the failure event
- Issue decisions should connect to the sprint that opened and resolved them
- Architectural decisions should connect to sprint records that validated them

### 5. Staleness Check

```bash
# Decisions not reviewed in >14 days (adjust threshold from config.yaml)
# This requires checking last_reviewed date against today
```

- Is `meta_state: current` accurate? Has anything happened since last_reviewed that would change this?
- Is `status: open` still accurate for issue decisions? Has a sprint resolved this?

### 6. Register Membership

Every decision should appear in at least one decision register. Orphan decisions (not in any register) lose value rapidly.

---

## Workflow

### 1. Read Target Decision(s)

Read fully. Do not skim.

### 2. Apply All Review Dimensions

For each decision, score each dimension: PASS / WARN / FAIL

| Dimension | Status | Notes |
|-----------|--------|-------|
| Schema compliance | PASS/WARN/FAIL | Missing fields |
| Title (claim test) | PASS/WARN/FAIL | Issue |
| Body (reasoning test) | PASS/WARN/FAIL | Issue |
| Connection completeness | PASS/WARN/FAIL | Missing connections |
| Staleness | PASS/WARN/FAIL | Days since reviewed |
| Register membership | PASS/WARN/FAIL | Which registers |

### 3. Propose Fixes

For each FAIL or WARN, propose the specific fix needed. Do not auto-apply.

### 4. Output Report

```
## Review Complete

### [[decision name]]

Schema: PASS
Title (claim test): WARN — title is noun phrase not claim
Body: PASS — 230 words, uses because/therefore
Connections: FAIL — no link to sprint that discovered this fact
Staleness: WARN — last_reviewed 18 days ago
Register: PASS — in [[qftest-register]]

Proposed fixes:
1. Title: change to "QFTest interpreter requires Groovy not groovy casing"
2. Connection: add "[[sprint-3-record]] — surfaces: QFTest discovered casing requirement"
3. Update last_reviewed to today

Overall: 2 issues require fix before this decision is trustworthy.

---

### Summary

Decisions reviewed: N
- PASS (no issues): N
- WARN (minor issues): N
- FAIL (requires fix): N

Most common issue: [description]
```

---

## Auto-Fix Policy

/pm-review proposes fixes but does NOT auto-apply them for body changes (human judgment required for reasoning).

/pm-review MAY auto-apply:
- `last_reviewed` date updates (mechanical, no judgment)
- Missing `meta_state` or `status` where the value is unambiguous

/pm-review MUST NOT auto-apply:
- Title rewrites (requires understanding the claim)
- Body changes (requires reasoning judgment)
- Status changes (requires sprint evidence verification)
